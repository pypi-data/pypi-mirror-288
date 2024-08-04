## 1.27.2 - 2024-08-03
### Extractors
#### Additions
- [agnph] add `tag` and `post` extractors ([#5284](https://github.com/mikf/gallery-dl/issues/5284), [#5890](https://github.com/mikf/gallery-dl/issues/5890))
- [aryion] add `favorite` extractor ([#4511](https://github.com/mikf/gallery-dl/issues/4511), [#5870](https://github.com/mikf/gallery-dl/issues/5870))
- [cien] add support ([#2885](https://github.com/mikf/gallery-dl/issues/2885), [#4103](https://github.com/mikf/gallery-dl/issues/4103), [#5240](https://github.com/mikf/gallery-dl/issues/5240))
- [instagram] add `info` extractor ([#5262](https://github.com/mikf/gallery-dl/issues/5262))
- [koharu] add `gallery`, `search`, and `favorite` extractors ([#5893](https://github.com/mikf/gallery-dl/issues/5893), [#4707](https://github.com/mikf/gallery-dl/issues/4707))
- [twitter] add `info` extractor ([#3623](https://github.com/mikf/gallery-dl/issues/3623))
#### Fixes
- [8chan] update `TOS` cookie name ([#5868](https://github.com/mikf/gallery-dl/issues/5868))
- [behance] fix image extraction ([#5873](https://github.com/mikf/gallery-dl/issues/5873), [#5926](https://github.com/mikf/gallery-dl/issues/5926))
- [booru] prevent crash when file URL is empty ([#5859](https://github.com/mikf/gallery-dl/issues/5859))
- [deviantart] try to work around journal/status API changes ([#5916](https://github.com/mikf/gallery-dl/issues/5916))
- [hentainexus] fix error with spread pages ([#5827](https://github.com/mikf/gallery-dl/issues/5827))
- [hotleak] fix faulty image URLs ([#5915](https://github.com/mikf/gallery-dl/issues/5915))
- [inkbunny:following] fix potentially infinite loop
- [nijie] fix image URLs of single image posts ([#5842](https://github.com/mikf/gallery-dl/issues/5842))
- [readcomiconline] fix extraction ([#5866](https://github.com/mikf/gallery-dl/issues/5866))
- [toyhouse] fix Content Warning bypass ([#5820](https://github.com/mikf/gallery-dl/issues/5820))
- [tumblr] revert to `offset` pagination, implement `pagination` option ([#5880](https://github.com/mikf/gallery-dl/issues/5880))
- [twitter] fix `username-alt` option name ([#5715](https://github.com/mikf/gallery-dl/issues/5715))
- [warosu] fix extraction
- [zerochan] handle `KeyError - 'items'` ([#5826](https://github.com/mikf/gallery-dl/issues/5826))
- [zerochan] fix error on tag redirections ([#5891](https://github.com/mikf/gallery-dl/issues/5891))
- [zerochan] fix `Invalid control character` errors ([#5892](https://github.com/mikf/gallery-dl/issues/5892))
#### Improvements
- [bunkr] support `bunkr.fi` domain ([#5872](https://github.com/mikf/gallery-dl/issues/5872))
- [deviantart:following] use OAuth API endpoint ([#2511](https://github.com/mikf/gallery-dl/issues/2511))
- [directlink] extend recognized file extensions ([#5924](https://github.com/mikf/gallery-dl/issues/5924))
- [exhentai] improve error message when temporarily banned ([#5845](https://github.com/mikf/gallery-dl/issues/5845))
- [gelbooru_v02] use total number of posts as pagination end marker ([#5830](https://github.com/mikf/gallery-dl/issues/5830))
- [imagefap] add enumeration index to default filenames ([#1746](https://github.com/mikf/gallery-dl/issues/1746), [#5887](https://github.com/mikf/gallery-dl/issues/5887))
- [paheal] implement fast `--range` support ([#5905](https://github.com/mikf/gallery-dl/issues/5905))
- [redgifs] support URLs with numeric IDs ([#5898](https://github.com/mikf/gallery-dl/issues/5898), [#5899](https://github.com/mikf/gallery-dl/issues/5899))
- [sankaku] match URLs with `www` subdomain ([#5907](https://github.com/mikf/gallery-dl/issues/5907))
- [sankakucomplex] update domain to `news.sankakucomplex.com`
- [twitter] implement `cursor` support ([#5753](https://github.com/mikf/gallery-dl/issues/5753))
- [vipergirls] improve `thread` URL pattern
- [wallpapercave] support `album` listings ([#5925](https://github.com/mikf/gallery-dl/issues/5925))
#### Metadata
- [dynastyscans] extract chapter `tags` ([#5904](https://github.com/mikf/gallery-dl/issues/5904))
- [erome] extract `date` metadata ([#5796](https://github.com/mikf/gallery-dl/issues/5796))
- [furaffinity] extract `folders` and `thumbnail` metadata ([#1284](https://github.com/mikf/gallery-dl/issues/1284), [#5824](https://github.com/mikf/gallery-dl/issues/5824))
- [sankaku] implement `notes` extraction ([#5865](https://github.com/mikf/gallery-dl/issues/5865))
- [subscribestar] fix `date` parsing in updated posts ([#5783](https://github.com/mikf/gallery-dl/issues/5783))
- [twitter] extract `bookmark_count` and `view_count` metadata ([#5802](https://github.com/mikf/gallery-dl/issues/5802))
- [zerochan] fix `source` metadata
- [zerochan] fix tag category extraction ([#5874](https://github.com/mikf/gallery-dl/issues/5874))
- [zerochan] delay fetching extended metadata ([#5869](https://github.com/mikf/gallery-dl/issues/5869))
#### Options
- [agnph] implement `tags` option ([#5284](https://github.com/mikf/gallery-dl/issues/5284))
- [booru] allow multiple `url` keys ([#5859](https://github.com/mikf/gallery-dl/issues/5859))
- [cien] add `files` option ([#2885](https://github.com/mikf/gallery-dl/issues/2885))
- [koharu] add `cbz` and `format` options ([#5893](https://github.com/mikf/gallery-dl/issues/5893))
- [vsco] add `include` option ([#5911](https://github.com/mikf/gallery-dl/issues/5911))
- [zerochan] implement `tags` option ([#5874](https://github.com/mikf/gallery-dl/issues/5874))
#### Removals
- [fallenangels] remove module
### Post Processors
- [metadata] allow using format strings for `directory` ([#5728](https://github.com/mikf/gallery-dl/issues/5728))
### Options
- add `--print-traffic` command-line option
- add `-J/--resolve-json` command-line option ([#5864](https://github.com/mikf/gallery-dl/issues/5864))
- add `filters-environment` option
- implement `archive-event` option ([#5784](https://github.com/mikf/gallery-dl/issues/5784))
### Actions
- [actions] support multiple actions per pattern
- [actions] add `exec` action ([#5619](https://github.com/mikf/gallery-dl/issues/5619))
- [actions] add `abort` and `terminate` actions ([#5778](https://github.com/mikf/gallery-dl/issues/5778))
- [actions] allow setting a duration for `wait`
- [actions] emit logging messages before waiting/exiting/etc
### Tests
- [tests] enable test results for external extractors ([#5262](https://github.com/mikf/gallery-dl/issues/5262))
- [tests] load results from `${GDL_TEST_RESULTS}` ([#5262](https://github.com/mikf/gallery-dl/issues/5262))
### Miscellaneous
- [cookies] add `thorium` support ([#5781](https://github.com/mikf/gallery-dl/issues/5781))
- [job] add `resolve` argument to DataJob ([#5864](https://github.com/mikf/gallery-dl/issues/5864))
- [path] fix moving temporary files across drives on Windows ([#5807](https://github.com/mikf/gallery-dl/issues/5807))
- [ytdl] fix `--cookies-from-browser` option parsing ([#5885](https://github.com/mikf/gallery-dl/issues/5885))
- make exceptions in filters/conditionals non-fatal
- update default User-Agent header to Firefox 128 ESR
- include `zstd` in Accept-Encoding header when supported
