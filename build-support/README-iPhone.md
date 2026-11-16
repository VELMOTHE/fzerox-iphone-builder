# F-Zero X f iPhone — personal build
Had package fih F0X-v0.1.2-ios-personal.ipa, ROM-converter.html, w build review.
Native arm64 device app, iOS16+; physical iPhone gameplay still needs your test.
This is a personal build, not a publicly cleared release.

## 1. Installer l'app
1. F Mac/Windows PC dyalk, telecharge Sideloadly mn https://sideloadly.io/
2. Rbet iPhone b cable, 7ell l'ecran, w dghat Trust ila tlebha.
3. Jer fichier .ipa l Sideloadly, khtar iPhone, dkhel Apple ID dyalk, w Start.
4. Ila tleb Trust: Settings > General > VPN & Device Management > Apple ID > Trust.
5. Ila tleb Developer Mode: Settings > Privacy & Security > Developer Mode.
L'IPA unsigned. Sideloadly kaydir signature b Apple ID dyalk.
B Apple ID gratuit, signature katdoum 7 iyam; t9der tjededha b Sideloadly.

## 2. Convert game data
1. 7ell ZIP l'asli li sifti: F-Zero X (USA).zip. Ghadi ykhrj fichier .n64.
2. 7ell ROM-converter.html f navigateur dyal Mac/PC.
3. Khtar fichier .n64 w dghat Convert and download .z64.
4. L'outil kayverifi USA rev0 SHA1, w kaykhrj FZeroX_USA_rev0.z64.
5. Sift .z64 l Files dyal iPhone b AirDrop wela iCloud Drive.
Conversion katوقع local, bla upload.

## 3. Launch
7ell F0X > Choose ROM... > khtar .z64 > Build game data and continue.
Jreb course wa7da: steering, acceleration, boost w audio.

## Build provenance
Source: https://github.com/chrissotraidis/f0x/tree/v0.1.2
Builder: https://github.com/VELMOTHE/fzerox-iphone-builder/tree/iphone-intel-build
Public release audit still reports 232 address-named binary symbols. See
PERSONAL_BUILD_REVIEW.json for the complete native source-definition mapping.
The device package is separately checked for arm64/iPhoneOS, resources and no ROM/signing secrets.
No gameplay modifications are included. Physical iPhone runtime is not verified by this build.
