#!/bin/bash
if [ ! -f ./deploy.lck ]; then
        echo locked > deploy.lck
        count=`ls -1 build_temp/*.zip 2>/dev/null | wc -l`
        if [ $count != 0 ]; then
                if [ -f build_temp/*_app.zip ]; then
                        rm -Rf /var/www/html/app/*
                        unzip -o build_temp/*_app.zip -d /var/www/html/app/
                        cp config/env.html /var/www/html/app/
                        find ./build_temp -type f -iname "*_app.zip" -print0 | while IFS= read -r -d $'\0' line; do
                                FILE="${line##*/}"
                                echo "${FILE%%_*}" > /var/www/html/app/p2aui_build_number.txt
                        done
                        rm build_temp/*_app.zip
                fi
                if [ -f build_temp/*_coverage.zip ]; then
                        rm -Rf /var/www/html/app/coverage
                        unzip build_temp/*_coverage.zip -d /var/www/html/app/coverage
                        rm build_temp/*_coverage.zip
                fi
        fi
        rm deploy.lck
        rm -f build_temp/.done
else
        echo "No action required. Exiting"
fi
