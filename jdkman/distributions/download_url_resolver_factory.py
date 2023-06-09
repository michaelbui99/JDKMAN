from jdkman.distributions.supported_distributions import SupportedDistribution
from jdkman.distributions.azul_zulu.zulu_download_url_resolver import ZuluDownloadUrlResolver as AzulZuluDownloadUrlResolver
from .download_url_resolver import DownloadUrlResolver


class DownloadUrlResolverFactory:
    def get_resolver(self, distribution: SupportedDistribution) -> DownloadUrlResolver:
        match distribution:
            case SupportedDistribution.ZULU:
                return AzulZuluDownloadUrlResolver()
