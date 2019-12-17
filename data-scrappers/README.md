# data-scrappers
This includes some scripts which were used to collect news articles from sinhala web news websites.

Following is the schema for the MySQL table.
```
CREATE TABLE `newsarticles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(50) COLLATE utf8_sinhala_ci NOT NULL,
  `sid` varchar(50) COLLATE utf8_sinhala_ci NOT NULL,
  `time` datetime NOT NULL,
  `title` text COLLATE utf8_sinhala_ci NOT NULL,
  `body` text COLLATE utf8_sinhala_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `source` (`source`,`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_sinhala_ci;
```