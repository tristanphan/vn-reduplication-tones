#!/bin/zsh
printf "This will clear all corpora, tools, virtual environments, results, etc. Proceed? (y/N) "
read -r yn

if [[ $yn != "y" ]]
then
    exit 1
fi

sudo rm -rf venv JVnTextPro Leipzig sentences.* reduplicates.* distribution_matrix.*