import marimo

__generated_with = "0.8.18"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import asyncio
    from crawl4ai import AsyncWebCrawler
    return AsyncWebCrawler, asyncio, mo


@app.cell
def __(AsyncWebCrawler):
    async def main():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/research/alignment-faking",
            )
            print(result.markdown)
            
    return (main,)


@app.cell
async def __(main, mo):
    with mo.status.spinner(title="Running prompt..."):
        await main()
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
