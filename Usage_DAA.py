import pandas as pd
from arcgis.gis import GIS

def get_group_items_info(group_id):
    # Connect to ArcGIS Online in anonymous mode
    gis = GIS()

    # Get the ArcGIS Online group for DAA Content
    group = gis.groups.get(group_id)

    # Get all items in the group
    items = group.content()

    # Initialize lists to store item information
    item_ids = []
    item_titles = []
    item_types = [] 
    item_hyperlinks = []
    item_total_views = []
    item_usage_7d = []
    item_owners = []

    # Loop through each item and collect information
    for item in items:
        item_ids.append(item.id)
        item_titles.append(item.title)
        item_types.append(item.type)
        item_hyperlinks.append(item.homepage)
        item_total_views.append(item.numViews)

        # Get the item owner's username
        item_owner = gis.users.get(item.owner)
        item_owners.append(item_owner.username)

        # Get the usage for the past 7 days - only works if you are Admin or item owner
        # try:
        #     item_usage_7d.append(item.usage('60D'))
        # except Exception as e:
        #     item_usage_7d.append("Not Available")

    # Create a pandas DataFrame to store the collected information
    data = {
        'Item ID': item_ids,
        'Title': item_titles,
        'Item Type': item_types,
        'Hyperlink': item_hyperlinks,
        'Total Views': item_total_views,
        #'Usage (60D)': item_usage_7d,
        'Owner': item_owners
    }
    df = pd.DataFrame(data)

    # Sort the DataFrame based on "Total Views" column in descending order
    df.sort_values(by='Total Views', ascending=False, inplace=True)
    
    return df



def generate_csv(dataframe, output_file):
    # Save DataFrame as CSV file
    dataframe.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Replace the following with the public ArcGIS Online group ID
    group_id = "c5f340b722ea4f8dafe87d3dcc80956f"

    item_table = get_group_items_info(group_id)

    # Replace "output_table.csv" with the desired output file name
    output_file_name = "DAA_Usage_Stats.csv"
    generate_csv(item_table, output_file_name)

    print(f"Table has been saved to '{output_file_name}'")