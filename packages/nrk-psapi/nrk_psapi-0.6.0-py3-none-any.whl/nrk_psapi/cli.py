"""nrk-psapi cli tool."""

import argparse
import asyncio
import logging

from rich import print as rprint

from nrk_psapi import NrkPodcastAPI
from nrk_psapi.models.pages import IncludedSection
from nrk_psapi.models.search import SearchType


def single_letter(string):
    return string[:1].upper()

def main_parser() -> argparse.ArgumentParser:  # noqa: PLR0915
    """Create the ArgumentParser with all relevant subparsers."""
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='A simple executable to use and test the library.')

    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    get_podcasts_parser = subparsers.add_parser('get_all_podcasts', description='Get all podcasts.')
    get_podcasts_parser.set_defaults(func=get_all_podcasts)

    browse_parser = subparsers.add_parser('browse', description='Browse podcast(s).')
    browse_parser.add_argument('letter', type=single_letter, help='The letter to browse.')
    browse_parser.add_argument('--limit', type=int, default=10, help='The number of results to return per page.')
    browse_parser.add_argument('--page', type=int, default=1, help='The page number to return.')
    browse_parser.set_defaults(func=browse)

    get_channel_parser = subparsers.add_parser('get_channel', description='Get channel.')
    get_channel_parser.add_argument('channel_id', type=str, help='The channel id.')
    get_channel_parser.set_defaults(func=get_channel)

    get_podcast_parser = subparsers.add_parser('get_podcast', description='Get podcast(s).')
    get_podcast_parser.add_argument('podcast_id', type=str, nargs="+", help='The podcast id(s).')
    get_podcast_parser.set_defaults(func=get_podcast)

    get_podcast_season_parser = subparsers.add_parser('get_podcast_season', description='Get podcast season.')
    get_podcast_season_parser.add_argument('podcast_id', type=str, help='The podcast id.')
    get_podcast_season_parser.add_argument('season_id', type=str, help='The season id.')
    get_podcast_season_parser.set_defaults(func=get_podcast_season)

    get_podcast_episodes_parser = subparsers.add_parser('get_podcast_episodes', description='Get podcast episodes.')
    get_podcast_episodes_parser.add_argument('podcast_id', type=str, help='The podcast id.')
    get_podcast_episodes_parser.add_argument('--season_id', type=str, required=False, help='The season id.')
    get_podcast_episodes_parser.set_defaults(func=get_podcast_episodes)

    get_series_parser = subparsers.add_parser('get_series', description='Get series.')
    get_series_parser.add_argument('series_id', type=str, help='The series id.')
    get_series_parser.set_defaults(func=get_series)

    get_episode_parser = subparsers.add_parser('get_episode', description='Get episode.')
    get_episode_parser.add_argument('podcast_id', type=str, help='The podcast id.')
    get_episode_parser.add_argument('episode_id', type=str, help='The episode id.')
    get_episode_parser.set_defaults(func=get_episode)

    get_episode_manifest_parser = subparsers.add_parser('get_episode_manifest', description='Get episode manifest.')
    get_episode_manifest_parser.add_argument('episode_id', type=str, help='The episode id.')
    get_episode_manifest_parser.set_defaults(func=get_manifest)

    get_episode_metadata_parser = subparsers.add_parser('get_episode_metadata', description='Get episode metadata.')
    get_episode_metadata_parser.add_argument('episode_id', type=str, help='The episode id.')
    get_episode_metadata_parser.set_defaults(func=get_metadata)

    get_curated_podcasts_parser = subparsers.add_parser('get_curated_podcasts', description='Get curated podcasts.')
    get_curated_podcasts_parser.set_defaults(func=get_curated_podcasts)

    get_pages_parser = subparsers.add_parser('get_pages', description='Get pages.')
    get_pages_parser.set_defaults(func=get_pages)

    get_page_parser = subparsers.add_parser('get_page', description='Get page content.')
    get_page_parser.add_argument('page_id', type=str, help='The page id.')
    get_page_parser.set_defaults(func=get_page)

    get_recommendations_parser = subparsers.add_parser('get_recommendations', description='Get recommendations.')
    get_recommendations_parser.add_argument('podcast_id', type=str, help='The podcast id.')
    get_recommendations_parser.set_defaults(func=get_recommendations)

    search_parser = subparsers.add_parser('search', description='Search.')
    search_parser.add_argument('query', type=str, help='The search query.')
    search_parser.add_argument('--type', type=SearchType, help='The search type.')
    search_parser.add_argument('--limit', type=int, default=10, help='The number of results to return per page.')
    search_parser.add_argument('--page', type=int, default=1, help='The page number to return.')
    search_parser.set_defaults(func=search)

    return parser


async def get_all_podcasts():
    """Get all podcasts."""
    async with NrkPodcastAPI() as client:
        podcasts = await client.get_all_podcasts()
        rprint(podcasts)


async def browse(args):
    """Browse podcast(s)."""
    async with NrkPodcastAPI() as client:
        results = await client.browse(args.letter, per_page=args.limit, page=args.page)
        rprint(results)


async def get_channel(args):
    """Get channel."""
    async with NrkPodcastAPI() as client:
        channel = await client.get_live_channel(args.channel_id)
        rprint(channel)


async def get_podcast(args):
    """Get podcast(s)."""
    async with NrkPodcastAPI() as client:
        podcasts = await client.get_podcasts(args.podcast_id)
        for podcast in podcasts:
            rprint(podcast)


async def get_podcast_season(args):
    """Get podcast season."""
    async with NrkPodcastAPI() as client:
        season = await client.get_podcast_season(args.podcast_id, args.season_id)
        rprint(season)


async def get_podcast_episodes(args):
    """Get podcast episodes."""
    async with NrkPodcastAPI() as client:
        episodes = await client.get_podcast_episodes(args.podcast_id, args.season_id)
        for episode in episodes:
            rprint(episode)


async def get_series(args):
    """Get series."""
    async with NrkPodcastAPI() as client:
        series = await client.get_series(args.series_id)
        rprint(series)


async def get_recommendations(args):
    """Get recommendations."""
    async with NrkPodcastAPI() as client:
        recommendations = await client.get_recommendations(args.podcast_id)
        rprint(recommendations)


async def get_episode(args):
    """Get episode."""
    async with NrkPodcastAPI() as client:
        episode = await client.get_episode(args.podcast_id, args.episode_id)
        rprint(episode)


async def get_manifest(args):
    """Get manifest."""
    async with NrkPodcastAPI() as client:
        manifest = await client.get_playback_manifest(args.episode_id)
        rprint(manifest)


async def get_metadata(args):
    """Get metadata."""
    async with NrkPodcastAPI() as client:
        metadata = await client.get_playback_metadata(args.episode_id)
        rprint(metadata)


async def get_curated_podcasts(args):
    """Get curated podcasts."""
    async with NrkPodcastAPI() as client:
        curated = await client.curated_podcasts()
        for section in curated.sections:
            rprint(f"# {section.title}")
            for podcast in section.podcasts:
                rprint(f"  - {podcast.title} ({podcast.id})")


async def get_pages(args):
    """Get radio pages."""
    async with NrkPodcastAPI() as client:
        radio_pages = await client.radio_pages()
        rprint("# Radio pages")
        for p in radio_pages.pages:
            page = await client.radio_page(p.id)
            rprint(f"# {page.title}")
            for section in page.sections:
                if isinstance(section, IncludedSection):
                    rprint(f"## {section.included.title}")
                    for plug in section.included.plugs:
                        rprint(f" - {plug!s}")
            rprint("")


async def get_page(args):
    """Get radio page."""
    async with NrkPodcastAPI() as client:
        page = await client.radio_page(args.page_id)
        rprint(f"# {page.title}")
        for section in page.sections:
            if isinstance(section, IncludedSection):
                rprint(f"## {section.included.title}")
                for plug in section.included.plugs:
                    rprint(f" - {plug!s}")


async def search(args):
    """Search."""
    async with NrkPodcastAPI() as client:
        results = await client.search(args.query, per_page=args.limit, page=args.page, search_type=args.type)
        rprint(results)


def main():
    """Run."""
    parser = main_parser()
    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == '__main__':
    main()
