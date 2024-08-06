import os
import sys
import json
import requests
import copy
import aiohttp
import asyncio

search_api_url = "https://claimminer.societylibrary.org/api/search"


def get_claimminer_api_token():
    # Fetch the password from environment variable
    password = os.environ.get("CLAIMMINER_PASSWORD")
    username = os.environ.get("CLAIMMINER_USERNAME")

    if not password:
        raise ValueError("Please set the CLAIMMINER_PASSWORD environment variable")

    # URL to get the access token
    token_url = "https://claimminer.societylibrary.org/api/token"

    # Data for the token request
    data = {"grant_type": "", "username": username, "password": password}

    # Request to get the access token
    response = requests.post(token_url, data=data)
    response_data = response.json()
    access_token = response_data.get("access_token")

    if not access_token:
        raise ValueError("Failed to retrieve access token")

    return access_token


# URLs & Endpoints
# Retrieve Access Token
try:
    access_token = get_claimminer_api_token()
    claimminer_available = True
except ValueError as e:
    print(f"Warning: {e}. ClaimMiner functionality will be disabled.")
    access_token = None
    claimminer_available = False

if access_token:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
else:
    headers = {
        "Accept": "application/json",
    }


def prepend_text(data):
    # Prepend question text
    data["question"] = "[question] " + data["question"]

    for position in data["positions"]:
        # Prepend position text
        position["position"] = "[position] " + position["position"]

        for category in position["categories"]:
            # Prepend category text
            category["category"] = "[category] " + category["category"]

            for claim in category["claims"]:
                # Prepend claim text
                claim["claim"] = "[including reasons like] " + claim["claim"]

                for i in range(len(claim["arguments"])):
                    # Prepend argument text
                    claim["arguments"][i] = (
                        "[to be more specific this means] " + claim["arguments"][i]
                    )


async def get_document_url_async(doc_id, session):
    if not claimminer_available:
        print("ClaimMiner is not available.")
        return None

    document_url = f"https://claimminer.societylibrary.org/api/document/{doc_id}"
    async with session.get(document_url, headers=headers) as response:
        if response.ok:
            document_info = await response.json()
            return document_info["url"]
        else:
            print(f"Error fetching document URL: {response.status} - {response.reason}")
            return None


# Function to search each claim and print the claim along with the top result
async def search_claimminer(text, cutoff=0.7):

    if not claimminer_available:
        print("ClaimMiner is not available.")
        return []

    form_data = {
        "search_text": text,
        "offset": 0,
        "limit": 10,
        "mode": "semantic",
        "model": "all_minilm_l6_v2",
        "lam": 0.7,
        "include_paragraphs": "true",
        "include_statements": "false",
        "one_per_doc": "false",
        "one_per_cluster": "false",
        "group_by_cluster": "false",
        "only_with_quote": "false",
        "include_sentences": "true",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            search_api_url, headers=headers, data=form_data
        ) as response:
            structured_results = []

            if response.ok:
                results = await response.json()

                if results:
                    top_result = results[0]
                    top_result_text = top_result["result"]["text"]
                    top_result_rank = top_result["rank"]
                    # print(f"Claim: {text}\nTop Result: {top_result_text}\nRank: {top_result_rank}\n")
                else:
                    print(f"No results found for the claim: {text}")

                for result in results:
                    top_result_rank = result["rank"]
                    if top_result_rank > cutoff:
                        doc_id = result["result"]["doc_id"]
                        document_url = await get_document_url_async(doc_id, session)
                        # print(document_url)
                        # print(result['result']['text'])
                        # print(text)
                        if document_url:
                            result_object = {
                                "quote": result["result"]["text"],
                                "url": document_url,
                                "similarity_score": top_result_rank,
                                "index": "claimminer",
                                "source_type": "claimminer",  # added to track source in bifocal browser
                                "full_text": result["result"][
                                    "text"
                                ],  # added full text to result object to be like other sources
                            }
                            structured_results.append(result_object)
            else:
                print(
                    f"Error searching the text: {response.status} - {response.reason}"
                )

    return structured_results


async def process_directory(debate_maps_folder="debate maps/documentary/todo"):

    # Loop through each file in the given directory
    for file in os.listdir(debate_maps_folder):
        if file.endswith(".json"):
            json_file_path = os.path.join(debate_maps_folder, file)
            print(f"Processing: {json_file_path}")

            # Load the JSON file
            with open(json_file_path, "r") as json_file:
                debate_graph = json.load(json_file)

            # Apply processing to each debate graph
            for index, position_obj in enumerate(debate_graph["positions"]):
                position = position_obj["position"]
                search_results = await search_claimminer(position)
                print(search_results)
                sys.exit()
                reference_urls_set = set()
                if search_results:
                    for result in search_results:
                        if "url" in result:
                            reference_urls_set.add(result["url"])
                reference_urls = list(reference_urls_set)
                if reference_urls:
                    debate_graph["positions"][index]["reference_urls"] = reference_urls

            # prepend_text(debate_graph)

            # Prepare and save the updated JSON file
            new_file_name_parts = file.split(".json")
            new_file_name = f"{new_file_name_parts[0]} (with references).json"
            new_file_path = os.path.join(debate_maps_folder, new_file_name)

            with open(new_file_path, "w") as new_json_file:
                json.dump(debate_graph, new_json_file, indent=4)

            print(f"Updated debate graph saved to '{new_file_name}'")

            # Make a deep copy of the debate_graph (so original is unchanged)
            debate_graph_no_refs = copy.deepcopy(debate_graph)

            # Visit each position and remove 'reference_urls'
            for position_obj in debate_graph_no_refs["positions"]:
                if "reference_urls" in position_obj:
                    del position_obj["reference_urls"]

            # Specify the path for the "no_reference" folder or create it if it doesn't exist
            no_ref_folder = os.path.join(debate_maps_folder, "no_reference")
            if not os.path.exists(no_ref_folder):
                os.makedirs(no_ref_folder)

            # Prepare the filename with the suffix "(with labels)" for saving without reference URLs
            original_file_name_without_extension = os.path.splitext(file)[0]
            no_ref_file_name = (
                f"{original_file_name_without_extension} (with labels).json"
            )
            no_ref_file_path = os.path.join(no_ref_folder, no_ref_file_name)

            # Save the modified copy without reference URLs but with the new suffix
            with open(no_ref_file_path, "w") as no_ref_json_file:
                json.dump(debate_graph_no_refs, no_ref_json_file, indent=4)

            print(f"Debate graph saved to '{no_ref_file_path}'")


if __name__ == "__main__":
    default_claim = (
        "Artificial intelligence will revolutionize the healthcare industry."
    )
    claim_input = input(
        f"Enter a claim to search in ClaimMiner (or press Enter to use the default claim '{default_claim}'): "
    )

    if not claim_input.strip():
        claim_input = default_claim

    async def search_and_print_results(claim):
        search_results = await search_claimminer(claim)
        print(f"Search results for the claim: {claim}")
        for result in search_results:
            print(f"Quote: {result['quote']}")
            print(f"URL: {result['url']}")
            print(f"Similarity Score: {result['similarity_score']}")
            print("---")

    asyncio.run(search_and_print_results(claim_input))

    """

    asyncio.run(process_directory())

    for index, position_obj in enumerate(debatege_graph['positions']):
        position = position_obj['position']
        reference_urls = search_text_and_print_top_result(position)
        if reference_urls:
            debate_graph['positions'][index]['reference_urls'] = reference_urls

    # Creating a new filename based on the existing one
    new_file_name_parts = debate_graph_file_name.split('.json')
    new_file_name = f"{new_file_name_parts[0]} (with references).json"

    prepend_text(debate_graph)

    # Save the updated `debate_graph` back to a new JSON file
    with open(new_file_name, 'w') as new_file:
        json.dump(debate_graph, new_file, indent=4)

    print(f"Updated debate graph saved to '{new_file_name}'")

    sys.exit()

    # Iterate through each position and category to extract claims
    for position in debate_graph['positions']:
        for category in position['categories']:
            for claim_obj in category['claims']:
                claim = claim_obj['claim']
                search_text_and_print_top_result(claim)

    """
