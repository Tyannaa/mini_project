# url = "http://dev.bootcamp.store.supersqa.com/",
# consumer_key = "ck_8169f43e770dc493cae77d7828e227835284050c",
# consumer_secret = "cs_581ae674c7298f39cf75d30523eb235b25bad1db",
# version = "wc/v3"

import argparse
import csv
from woocommerce import API


def get_all_products(url, consumer_key, consumer_secret):
    wcapi = API(
        url=url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3"
    )

    all_products = []
    page = 1
    per_page = 100

    while True:
        # Make the API call to retrieve products
        products = wcapi.get("products", params={"page": page, "per_page": per_page}).json()

        if len(products) == 0:
            break
        all_products.extend(products)
        page += 1

    return all_products


def filter_products_by_price(products, max_price):
    return [product for product in products if float(product['price']) < max_price]


def print_products_under_price(products):
    if not products:
        print("No products found under the specified price.")
    else:
        print("Products under the specified price:")
        for product in products:
            print(f"{product['name']} - Price: ${product['price']}")


def save_to_csv(products, filename):
    if not products:
        print("No products to save to CSV.")
    else:
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['Product Name', 'Price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow({'Product Name': product['name'], 'Price': product['price']})


def parse_arguments():
    parser = argparse.ArgumentParser(description='Get products priced under a certain amount from WooCommerce.')
    parser.add_argument('--url', type=str, default='http://dev.bootcamp.store.supersqa.com/',
                        help='WooCommerce website URL')
    parser.add_argument('--consumer_key', type=str, default='ck_8169f43e770dc493cae77d7828e227835284050c', help='WooCommerce API Consumer Key')
    parser.add_argument('--consumer_secret', type=str, default='cs_581ae674c7298f39cf75d30523eb235b25bad1db', help='WooCommerce API Consumer Secret')
    parser.add_argument('--price_cut', type=float, help='Maximum price for filtering products')
    parser.add_argument('--output_file', type=str, default='filtered_products.csv', help='Output CSV file name')
    return parser.parse_args()


def main():
    args = parse_arguments()

    url = args.url
    consumer_key = args.consumer_key
    consumer_secret = args.consumer_secret

    all_products = get_all_products(url, consumer_key, consumer_secret)

    max_price = args.price_cut if args.price_cut else 10  # Default maximum price is $10
    filtered_products = filter_products_by_price(all_products, max_price)

    print_products_under_price(filtered_products)

    filename = args.output_file
    save_to_csv(filtered_products, filename)


if __name__ == "__main__":
    main()
