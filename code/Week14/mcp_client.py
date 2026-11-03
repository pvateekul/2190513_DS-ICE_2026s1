from fastmcp import Client
import asyncio

from mcp_server import mcp


def main():
    async def run():
        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_top_provinces",
                {"column": "rainfall", "n": 3},
            )

        print(result)

    asyncio.run(run())


if __name__ == "__main__":
    main()
