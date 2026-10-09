#!/bin/bash
# Builds Kakitori for Android: a signed app bundle for Google Play and a signed APK for testing.
#
# Usage: build.sh <sdk dir> <keystore.p12> <keystore password> <output dir>
#
# <sdk dir> holds the official Android tools, no Gradle needed:
#   build-tools-36.1/   aapt2, d8, zipalign, apksigner   (build-tools 36.1 for Linux)
#   android-36/         android.jar                      (platform 36)
#   bundletool/         bundletool 1.18.3 and its jars    (com.android.tools.build:bundletool)
# Run tools/make_offline.py first so assets/index.html exists.
set -euo pipefail
SDK="$1"; KS="$2"; PW="$3"; OUT="$4"
BT="$SDK/build-tools-36.1"; AJ="$SDK/android-36/android.jar"
BUNDLETOOL=(java -cp "$SDK/bundletool/*" com.android.tools.build.bundletool.BundleToolMain)
ALIAS=renshu
LINK=(--manifest AndroidManifest.xml -I "$AJ" -A assets --min-sdk-version 26 --target-sdk-version 36 -0 html)

rm -rf build && mkdir -p build/classes build/dex build/base
"$BT/aapt2" compile --dir res -o build/res.zip

# Java -> dex
javac -source 8 -target 8 -bootclasspath "$AJ" -classpath "$AJ" -Xlint:-options -nowarn -d build/classes $(find src -name "*.java")
"$BT/d8" --release --min-api 26 --lib "$AJ" --output build/dex $(find build/classes -name "*.class")

# Test APK, for installing straight onto a phone
"$BT/aapt2" link -o build/unsigned.apk "${LINK[@]}" build/res.zip
(cd build/dex && zip -q ../unsigned.apk classes.dex)
"$BT/zipalign" -f -p 4 build/unsigned.apk build/aligned.apk
"$BT/apksigner" sign --ks "$KS" --ks-type PKCS12 --ks-key-alias "$ALIAS" --ks-pass "pass:$PW" --key-pass "pass:$PW" --out "$OUT/Kakitori.apk" build/aligned.apk
"$BT/apksigner" verify "$OUT/Kakitori.apk"

# App bundle for Google Play: the same app with resources in protobuf form, laid out as a "base" module
"$BT/aapt2" link --proto-format -o build/proto.apk "${LINK[@]}" build/res.zip
(cd build/base && unzip -q ../proto.apk && mkdir manifest dex && mv AndroidManifest.xml manifest/ && cp ../dex/classes.dex dex/ && zip -qr ../base.zip .)
"${BUNDLETOOL[@]}" build-bundle --modules=build/base.zip --output=build/Kakitori.aab
jarsigner -keystore "$KS" -storetype PKCS12 -storepass "$PW" -sigalg SHA256withRSA -digestalg SHA-256 -signedjar "$OUT/Kakitori.aab" build/Kakitori.aab "$ALIAS" > /dev/null
jarsigner -verify "$OUT/Kakitori.aab" | tail -1
echo "Built $OUT/Kakitori.apk and $OUT/Kakitori.aab"
