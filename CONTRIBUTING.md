# Contributing

Contributions are welcome!
- Bugfixes, performance improvements, and minor tweeks are especially welcome and don't need prior discussion.
- Changes that aim to allow better compatability with other packs are very welcome too!
- Larger changes such as new biomes are unlkely to be merged, since I want to keep controll over that.
    - I recommed creating your own add-on datapack instead. I am happy to help with compatability. 
    
Once the pack is out of beta, contributions that can cause chunk borders have to be carefully considered.


# Building
This datapack is build using [mcbeet](https://mcbeet.dev). The biome layout is build using [Snowcapped](https://github.com/jacobsjo/snowcapped).

### Installation:
```bash
pip install beet
npm i snowcapped
```

### Build
```bash
beet
```

To auto-update after changes:
```bash
beet watch
```

The compiled datapack can be found in the `build` folder.