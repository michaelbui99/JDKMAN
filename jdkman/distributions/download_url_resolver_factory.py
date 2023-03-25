from distributions.supported_distributions import SupportedDistribution
from distributions.azul_zulu.download_url_resolver import DownloadUrlResolver as AzulZuluDownloadUrlResolver


class DownloadUrlResolverFactory:
    @staticmethod
    def get_resolver(distribution: SupportedDistribution):
        match distribution:
            case SupportedDistribution.ZULU:
                return AzulZuluDownloadUrlResolver()
