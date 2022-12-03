from forta_agent import Finding, FindingType, FindingSeverity

from src.config import FUNDING_CRITICAL, FUNDING_HIGH, FUNDING_MEDIUM, LAUNDERING_CRITICAL, LAUNDERING_HIGH, \
    LAUNDERING_MEDIUM, LAUNDERING_LOW, FUNDING_LOW


def get_severity(usd):
    if usd > FUNDING_CRITICAL:
        return FindingSeverity.Critical
    elif usd > FUNDING_HIGH:
        return FindingSeverity.High
    elif usd > FUNDING_MEDIUM:
        return FindingSeverity.Medium
    elif usd > FUNDING_LOW:
        return FindingSeverity.Low
    else:
        return FindingSeverity.Info


def get_severity_laundering(usd):
    if usd > LAUNDERING_CRITICAL:
        return FindingSeverity.Critical
    elif usd > LAUNDERING_HIGH:
        return FindingSeverity.High
    elif usd > LAUNDERING_MEDIUM:
        return FindingSeverity.Medium
    elif usd > LAUNDERING_LOW:
        return FindingSeverity.Low
    else:
        return FindingSeverity.Info


class FundingLaunderingFindings:

    @staticmethod
    def funding(from_, to, usd, token, type_, tx_hash):
        return Finding({
            'name': f'Funding Alert',
            'description': f'{to} was funded using {type_ if not type_ == "unknown" else ""} {from_}',
            'alert_id': 'FLD_FUNDING',
            'severity': get_severity(usd),
            'type': FindingType.Suspicious if get_severity(usd) != FindingSeverity.Info else FindingType.Info,
            'metadata': {
                'funded_address': to,
                'source_address': from_,
                'source_type': type_,
                'usd_volume': usd,
                'token': token,
                'tx_hash': tx_hash,
            }
        })

    @staticmethod
    def laundering(from_, to, usd, token, is_new, type_, tx_hash):
        return Finding({
            'name': f'Laundering Alert',
            'description': f'{from_} is engaged in money laundering behavior using {type_ if not type_ == "unknown" else ""} {from_}',
            'alert_id': 'FLD_Laundering',
            'type': FindingType.Suspicious if get_severity_laundering(usd) != FindingSeverity.Info else FindingType.Info,
            'severity': get_severity_laundering(usd),
            'metadata': {
                'laundering_address': from_,
                'newly_created': is_new,
                'target_address': to,
                'target_type': type_,
                'usd_volume': usd,
                'token': token,
                'tx_hash': tx_hash,
            }
        })

    @staticmethod
    def funding_newly_created(from_, to, usd, token, type_, tx_hash):
        return Finding({
            'name': f'Newly Created Account Funding Alert',
            'description': f'new {to} was funded using {type_ if not type_ == "unknown" else ""} {from_}',
            'alert_id': 'FLD_NEW_FUNDING',
            'severity': FindingSeverity.Critical if type_ != 'exchange' or type_ != 'dex' else FindingSeverity.High,
            'type': FindingType.Suspicious,
            'metadata': {
                'funded_address': to,
                'source_address': from_,
                'source_type': type_,
                'usd_volume': usd,
                'token': token,
                'tx_hash': tx_hash,
            }
        })
