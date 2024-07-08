# Minecraft-Lang-updater
A tool for updating translations of minecraft mods

Imagine you have some minecraft mod, already translated.
In my example im using Butchery v2.4.2

You have a translated file, ru_ru.json for example (for russian translation).

Suddenly, mod author decides to add more items, so there is a new mod version,
in my example Butchery v2.4.7

It will be hard to look what line was added to the lang file (especially when there are 600+ shuffled lines), so this tool does it for you!

You need to specify:
    Path to the NEW en_us.json lang file (Or path to the new .jar mod file, it will find en_us.json itself)
    Path to the partly translated lang file, for old mod version (No matter what language .json, OR if it's a .jar it will look for specified lang)
    Path to the output file!

Example of input-output can be found in testdata folder