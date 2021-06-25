from snapflow_shopify.connector import ShopifyOrdersImporter


@datafunction(
    "import_orders",
    namespace="shopify",
    state_class=ImportShopifyOrdersState,
    display_name="Import Shopify orders",
)
def import_orders(ctx: Context, admin_url: str,) -> Iterator[Records[ShopifyOrder]]:
    importer = ShopifyOrdersImporter()
    while ctx.should_continue():
        resp = importer.get_data(
            url=endpoint_url
        )
        json_resp = resp.json_data
        has_next_page = resp.next_page
        assert isinstance(json_resp, dict)
        records = json_resp["orders"]
        if len(records) == 0:
            # All done
            break
        new_latest_updated_at = max([o["updated_at"] for o in records])
        ctx.emit_state({"latest_updated_at": new_latest_updated_at})
        yield records
        # Shopify has cursor-based pagination now, so we can safely paginate results
        next_page = get_next_page_link(resp.headers)
        if not next_page:
            # No more pages
            break
        endpoint_url = next_page
        params = {}