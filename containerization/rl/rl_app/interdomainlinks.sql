/*****************************SAMPLE DATA *****************************/
/*------------------ InterDomain Links -------------------------*/


/*----------------------------------DOM1-DOM5---------------------------*/

/*--------------------------------- LINK 1 –> DOM1-DOM3 --------------------*/

INSERT INTO `mtpdomdb`.`interdomainlink`
(`srcDomId`,
`dstDomId`,
`srcGwId`,
`dstGwId`,
`srcGWIp`,
`dstGwIp`,
`delay`,
`availableBandwidth`,
`reservedBandwidth`,
`totalBandwidth`,
`allocatedBandwidth`)
VALUES
(1,
 3,
"192.168.3.30", /*192.168.3.30*/
"10.7.4.16", /*192.168.1.10*/
"0.0.0.13",
"0.0.0.23",
"10",
"10000000",
"0",
"10000000",
"0");

/*--------------------------------- LINK 2 –> DOM3-DOM1 --------------------*/

INSERT INTO `mtpdomdb`.`interdomainlink`
(`srcDomId`,
`dstDomId`,
`srcGwId`,
`dstGwId`,
`srcGWIp`,
`dstGwIp`,
`delay`,
`availableBandwidth`,
`reservedBandwidth`,
`totalBandwidth`,
`allocatedBandwidth`)
VALUES
(3,
 1,
"10.7.4.16", /*192.168.1.10*/
"192.168.3.30", /*192.168.3.30*/
"0.0.0.23",
"0.0.0.13",
"10",
"10000000",
"0",
"10000000",
"0");




/*--------------------------------- LINK 3 –> DOM2-DOM3 --------------------*/

INSERT INTO `mtpdomdb`.`interdomainlink`
(`srcDomId`,
`dstDomId`,
`srcGwId`,
`dstGwId`,
`srcGWIp`,
`dstGwIp`,
`delay`,
`availableBandwidth`,
`reservedBandwidth`,
`totalBandwidth`,
`allocatedBandwidth`)
VALUES
(2,
 3,
"192.168.4.40", /*192.168.4.40*/
"10.7.4.3", /*192.168.1.20*/
"0.0.0.14",
"0.0.0.24",
"10",
"10000000",
"0",
"10000000",
"0");
/*--------------------------------- LINK 4 –> DOM3-DOM2 --------------------*/

INSERT INTO `mtpdomdb`.`interdomainlink`
(`srcDomId`,
`dstDomId`,
`srcGwId`,
`dstGwId`,
`srcGWIp`,
`dstGwIp`,
`delay`,
`availableBandwidth`,
`reservedBandwidth`,
`totalBandwidth`,
`allocatedBandwidth`)
VALUES
(3,
 2,
"10.7.4.3", /*192.168.1.20*/
"192.168.4.40", /*192.168.4.40*/
"0.0.0.24",
"0.0.0.14",
"10",
"10000000",
"0",
"10000000",
"0");


