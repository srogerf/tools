import os
import re
import shutil

INPUT_DIRECTORY='D:\\data\\local_cache\\guitar_pro_songs'

# list directory
standard_naming_pattern = '^([^-]*)\s*-\s*(.*)\.(.*)$'
FILES_TOTAL=0
FILES_MATCHED=0
FILES_UNMATCHED=0
ZIPS_FOUND=0
MAX=100000
count = 0
bands = {}

for path in os.listdir(INPUT_DIRECTORY):
    if(os.path.isfile(os.path.join(INPUT_DIRECTORY, path))):
        FILES_TOTAL = FILES_TOTAL + 1
        if(count > MAX):
            break
        if(path.endswith("zip")):
            ZIPS_FOUND = ZIPS_FOUND + 1
            if bands.get("zip_files") == None:
                bands["zip_files"] = {}
            bands['zip_files'][path] = path

        matches = re.search(standard_naming_pattern, path)
        if(matches):
            band = matches.group(1)
            song = matches.group(2)
            extension = matches.group(3)
            FILES_MATCHED = FILES_MATCHED + 1
            if bands.get(band) == None:
                bands[band] = {}
            bands[band][song] = path
            #print(f"band: {band} : \tsong: {song}, \toriginal name: {path}")
            count = count + 1
        else:
            FILES_UNMATCHED = FILES_UNMATCHED + 1
            print(f'\tUNMATCHED: {path}')

# sort well known files

#print (json.dumps(bands["Rush"], indent=4))

# make directories
name_matcher_pattern = "^(.*)\s*,\s*(.*)$"
for band in bands:
    fixed_band = band
    matches = re.search(name_matcher_pattern, band)
    if(matches):
        fixed_band = f"{matches.group(2)} {matches.group(1)}"

    fixed_band = re.sub(r"\s+", ' ', fixed_band)
    fixed_band = fixed_band.strip()
    path = os.path.join(INPUT_DIRECTORY, fixed_band)
    print(path)
    if(os.path.isdir(path) is False):
        os.mkdir(path, 0x666)

    for song in bands[band]:
        source = os.path.join(INPUT_DIRECTORY, bands[band][song])
        target = os.path.join(INPUT_DIRECTORY, fixed_band, bands[band][song])
        shutil.move(source, target)


print("---------")
print(f"Total bands {len(bands)}")
print(f"Total files {FILES_TOTAL}, Matched: {FILES_MATCHED}, Unmatched: {FILES_UNMATCHED}, Zips: {ZIPS_FOUND}")
print(f"Check match+unmatch: {FILES_MATCHED + FILES_MATCHED}, match ration: {FILES_MATCHED/FILES_TOTAL}")
