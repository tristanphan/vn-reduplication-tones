#!/bin/zsh
# Set up Python
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt

# Set up Leipzig Vietnamese corpora
(
    mkdir Leipzig
    cd Leipzig || exit
    leipzig_corpora=("vie_news_2022_1M" "vie_wikipedia_2021_1M" "vie-vn_web_2015_1M" "vie_mixed_2014_1M"
                     "vie_newscrwal_2011_1M" "vie_news_2020_1M" "vie_news_2019_300K" "vie_wikipedia_2016_1M")
    for i in "${leipzig_corpora[@]}"
    do
        wget "https://downloads.wortschatz-leipzig.de/corpora/${i}.tar.gz"
        number_of_top_level_elements=$(tar -tf "${i}.tar.gz" --exclude="*/?*" |
 wc -l)
        if [[ $number_of_top_level_elements -gt 1 ]]
        then
            # Create a new folder for contents if there are more than one top-level items
            mkdir "${i}"
            tar -xvf "${i}.tar.gz" --directory "${i}"
        else
            tar -xvf "${i}.tar.gz"
        fi
        rm "${i}.tar.gz"
    done
)

# Set up JVnTextPro
wget https://sourceforge.net/projects/jvntextpro/files/latest/download -O jvntextpro.zip
unzip jvntextpro.zip
mv JVnTextPro-v.2.0 JVnTextPro
rm jvntextpro.zip