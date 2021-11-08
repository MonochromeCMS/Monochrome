#!/bin/bash

rm -r dist
cd monochrome-webui
yarn
yarn build
mv dist ../
