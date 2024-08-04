from enum import Enum


class Site(str, Enum):
    pass


class NyaaSite(Site):
    NYAA_SI = 'https://nyaa.si'
    NYAA_EU = 'https://nyaa.eu'
    NYAA_INK = 'https://nyaa.ink'
    NYAA_LAND = 'https://nyaa.land'
    NYAA_DIGITAL = 'https://nyaa.digital'
    NYAA_ISS_ONE = 'https://nyaa.iss.one'


class SukebeiSite(Site):
    SUKEBEI_NYAA = 'https://sukebei.nyaa.si'
    SKB_NYAA_HACGN_EU = 'https://skb-nyaa.hacgn.eu.org'
