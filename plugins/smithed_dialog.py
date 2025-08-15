from beet import Context, Dialog, DialogTag

def beet_default(ctx: Context):

    ctx.data['smithed:data_packs'] = Dialog({
        "type": "minecraft:dialog_list",
        "external_title": {
            "translate": "menu.smithed.data_packs",
            "fallback": "%s...",
            "with": [
                {
                    "translate": "selectWorld.dataPacks"
                }
            ]
        },
        "title": {
            "translate": "menu.smithed.data_packs.title",
            "fallback": "%s",
            "with": [
                {
                    "translate": "selectWorld.dataPacks"
                }
            ]
        },
        "dialogs": "#smithed:data_packs",
        "exit_action": {
            "label": {
            "translate": "gui.back"
            },
            "width": 200
        }
    })

    ctx.data['minecraft:pause_screen_additions'] = DialogTag({
        "values": [
            {
                "id": "smithed:data_packs",
                "required": False
            }
        ]
    })

    ctx.data['smithed:data_packs'] = DialogTag({
        "values": [
            "lavaflow:about"
        ]
    })

    ctx.data['lavaflow:about'] = Dialog({
        "type": "minecraft:multi_action",
        "title": "Lavaflow",
        "body": [
            {
                "type": "minecraft:item",
                "item": {
                    "id": "minecraft:lava_bucket"
                },
                "width": 20,
                "height": 16,
                "show_decorations": False,
                "show_tooltip": False,
                "description": {
                    "contents": [
                        {
                            "text": "Lavaflow",
                            "color": "#ffc551"
                        },
                        {
                            "text": " by jacobsjo",
                            "color": "#8b8b8b"
                        },
                        "\n",
                        {
                            "text": "Overhauled nether",
                            "color": "#ffffff"
                        }
                    ],
                    "width": 300
                }
            },
            {
                "type": "minecraft:item",
                "item": {
                    "id": "minecraft:paper"
                },
                "width": 20,
                "height": 16,
                "show_decorations": False,
                "show_tooltip": False,
                "description": {
                    "contents": {
                        "text": f'v{ctx.project_version}' ,
                        "color": "gray"
                    },
                    "width": 300
                }
            },
            {
                "type": "minecraft:plain_message",
                "contents": {
                    "text": "Completely overhauled Nether: Lava rivers on 2 heights with lavafalls between them, proper valleys, oceans, and new biomes and structures."
                },
                "width": 500
            },
            {
                "type": "minecraft:plain_message",
                "contents": [
                    {
                        "text": "[Smithed]",
                        "color": "#3df149",
                        "click_event": {
                            "action": "open_url",
                            "url": "https://smithed.net/packs/lavaflow"
                        }
                    },
                    " ",
                    {
                        "text": "[Modrinth]",
                        "color": "#3df149",
                        "click_event": {
                            "action": "open_url",
                            "url": "https://modrinth.com/datapack/lavaflow"
                        }
                    },
                    " ",
                    {
                        "text": "[CurseForge]",
                        "color": "#3df149",
                        "click_event": {
                            "action": "open_url",
                            "url": "https://www.curseforge.com/minecraft/mc-mods/lavaflow"
                        }
                    },
                    " ",
                    {
                        "text": "[GitHub]",
                        "color": "#3df149",
                        "click_event": {
                            "action": "open_url",
                            "url": "https://github.com/jacobsjo/lavaflow"
                        }
                    }
                ],
                "width": 500
            },
            {
                "type": "minecraft:plain_message",
                "contents": "\n\n\n\n",
                "width": 10
            }
        ],
        "actions": [
            {
                "label": "Biome Map",
                "action": {
                    "type": "open_url",
                    "url": "https://map.jacobsjo.eu/?datapacks=modrinth:lavaflow&dimension=minecraft:the_nether"
                }
            },
            {
                "label": "Report Issue...",
                "action": {
                    "type": "open_url",
                    "url": "https://github.com/jacobsjo/lavaflow/issues"
                }
            },
            {
                "label": "Buy me a coffee",
                "action": {
                    "type": "open_url",
                    "url": "https://ko-fi.com/jacobsjo"
                }
            }
        ],
        "exit_action": {
            "action": {
                "type": "show_dialog",
                "dialog": "smithed:data_packs"
            },
            "label": {
                "translate": "gui.back"
            },
            "width": 200
        },
        "after_action": "none",
        "pause": False
    }
    )
