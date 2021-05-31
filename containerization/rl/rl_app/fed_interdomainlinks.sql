/*****************************SAMPLE DATA *****************************/
/*------------------ Federeted InterDomain Links -------------------------*/



INSERT INTO `mtpfeddb`.`fed_interdomainlink`
(`interDomainLinkId`,
`srcGwIp`,
`dstGwIp`,
`srcGwId`,
`dstGwId`,
`abstrSrcNfviPopId`,
`abstrDestNfviPopId`,
`delay`,
`cost`,
`totalBandwidth`,
`reservedBandwidth`,
`availableBandwidth`,
`networkLayer`,
`interNfviPopNetworkType`,
`interNfviPopNetworkTopology`)
VALUES
(1111,
"0.0.0.91",
"0.0.0.92",
"192.168.10.10",
"10.7.4.16",
91,
31,
"10",
"1",
"1000000",
"",
"1000000",
"",
"",
"");


INSERT INTO `mtpfeddb`.`fed_interdomainlink`
(`interDomainLinkId`,
`srcGwIp`,
`dstGwIp`,
`srcGwId`,
`dstGwId`,
`abstrSrcNfviPopId`,
`abstrDestNfviPopId`,
`delay`,
`cost`,
`totalBandwidth`,
`reservedBandwidth`,
`availableBandwidth`,
`networkLayer`,
`interNfviPopNetworkType`,
`interNfviPopNetworkTopology`)
VALUES
(1112,
"0.0.0.92",
"0.0.0.91",
"10.7.4.16",
"192.168.10.10",
31,
91,
"10",
"1",
"1000000",
"",
"1000000",
"",
"",
"");











