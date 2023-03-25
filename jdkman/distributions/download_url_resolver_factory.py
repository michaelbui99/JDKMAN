from distributions.supported_distributions import SupportedDistribution
from distributions.azul.download_url_resolver import DownloadUrlResolver as AzulDownloadUrlResolver


class DownloadUrlResolverFactory:
    @staticmethod
    def get_resolver(distribution: SupportedDistribution):
        match distribution:
            case SupportedDistribution.AZUL:
                return AzulDownloadUrlResolver()
