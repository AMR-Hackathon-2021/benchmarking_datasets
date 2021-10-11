# grab card cannonical data
echo "=================================== DOWNLOAD CARD CANONICAL DATA ==================================="
# get latest card database
wget -O data --no-check-certificate https://card.mcmaster.ca/latest/data
mkdir -p card_data
tar xf data -C card_data
rm data

echo "=================================== DOWNLOAD CARD VARIANTS DATA ==================================="
wget -O variants --no-check-certificate https://card.mcmaster.ca/latest/variants
mkdir -p card_variants
tar xf variants -C card_variants
gunzip card_variants/*.gz
rm variants
