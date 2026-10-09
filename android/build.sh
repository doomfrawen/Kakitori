#!/bin/bash
# Usage: build.sh <tools dir> <keystore.p12> <keystore password> <output.apk>
set -euo pipefail
T="$1"; KS="$2"; PW="$3"; OUT="$4"
AAPT="$T/aapt/package/bin/x64/linux/aapt2"; AJ="$T/sdk/android.jar"
chmod +x "$AAPT"
rm -rf build && mkdir -p build/compiled build/classes
"$AAPT" compile --dir res -o build/compiled/res.zip
"$AAPT" link -o build/base.apk -I "$AJ" --manifest AndroidManifest.xml -A assets build/compiled/res.zip --min-sdk-version 26 --target-sdk-version 34 -0 html
java -m jdk.compiler/com.sun.tools.javac.Main -source 8 -target 8 -bootclasspath "$AJ" -classpath "$AJ" -Xlint:-options -d build/classes $(find src -name "*.java")
(cd build/classes && java -m jdk.jartool/sun.tools.jar.Main cf ../classes.jar .)
bash "$T"/d2j/dex-tools-*/d2j-jar2dex.sh -f -o build/classes.dex build/classes.jar >/dev/null
cp build/base.apk build/unsigned.apk && (cd build && zip -q unsigned.apk classes.dex)
java -jar "$T/signer/uber-apk-signer-1.3.0.jar" -a build/unsigned.apk --ks "$KS" --ksAlias renshu --ksPass "$PW" --ksKeyPass "$PW" -o build/out | grep -E 'success|verified|error|ERROR|Subject|SHA256'
cp build/out/unsigned-aligned-signed.apk "$OUT"
