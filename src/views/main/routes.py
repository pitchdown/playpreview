import requests
from random import choice
from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from collections import Counter

from src.extensions import db
from src.models.models import Track, Artist, Album, user_artist, user_album, user_track
from src.functions import get_preview_url_if_null, token_required

main_bp = Blueprint('main', __name__)

<<<<<<< HEAD
tracks_list = [{'name': 'manna', 'id': '0NGCFZaKB4WgUooVaAW4l8', 'artists_name': 'babyfather',
                'artists_id': '3DmDJOQgrwlq8MxXGLeFvA', 'album': 'aug freestyle / manna',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27390acc689ef1a170f0e357ca1',
                'preview_url': 'https://p.scdn.co/mp3-preview/ac7369a071b43474697fe387958b0b3ac47a053d?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'loving furlong', 'id': '2s9j8TV8rqK73MxStehVTD', 'artists_name': 'bullion',
                'artists_id': '6vcPgFOkMWBoY6Ks6eMEWj', 'album': 'heaven is over',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c5a7a4e34c5e05e533c4184e',
                'preview_url': 'https://p.scdn.co/mp3-preview/f0b8f7c570541032569922afb1c5171844c8cedf?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'whaleshark', 'id': '3BsBD6gkwdutyI7RQP5Ea4', 'artists_name': 'king krule',
                'artists_id': '4wyNyxs74Ux8UIDopNjIai', 'album': 'shhhhhhh!',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2731fec7a0acee1454153dba5b5',
                'preview_url': 'https://p.scdn.co/mp3-preview/d1dbb22af6be3177eed64f6f1297b0d14600d2ba?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'annie, pick a flower.. (my house)', 'id': '72AeIPJXQxYgtOIcmSnvQo',
                'artists_name': 'saya gray', 'artists_id': '4EnymklUyqZwvmHQGlRssl',
                'album': 'annie, pick a flower.. (my house)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a396a8aa9c5d2e31b77440ac',
                'preview_url': 'https://p.scdn.co/mp3-preview/d7b31bcbe63a8b1e9e0da5528839edccaf222168?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': "it's nice to be alive", 'id': '2vVMA6goXUgJSKcnnQrgin', 'artists_name': 'vegyn',
                'artists_id': '5iUnvXddCpOrbWKm7QMr6o', 'album': 'only diamonds cut diamonds',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273de301906ddf37189b1998f16',
                'preview_url': 'https://p.scdn.co/mp3-preview/e7ef9631647776457e9c7145705384f460d29c4d?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'new star in the sky - demo 1', 'id': '0ty8rSBaDkNPWO8Ex4ifUO', 'artists_name': 'air',
                'artists_id': '1P6U1dCeHxPui5pIrGmndZ', 'album': 'moon safari rarities (25th anniversary edition)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c4027cea1ac0a27a6801f3cf',
                'preview_url': 'https://p.scdn.co/mp3-preview/c7e2632e1c4ecef0e1803a54b2c61a8da6dad245?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'treat each other right', 'id': '52GJf3163rfoCtjOvCe85K', 'artists_name': 'jamie xx',
                'artists_id': '7A0awCXkE1FtSU8B0qwOJQ', 'album': 'treat each other right',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27382d2f93d353c3c7d0828959c',
                'preview_url': 'https://p.scdn.co/mp3-preview/a518fdb34284daa9a2298fd5491d6cede24a3e01?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'staying here', 'id': '4gdM3XzcjeJQZPpMvuf9VF', 'artists_name': 'astrid sonne',
                'artists_id': '7qiyPneI60DzZmxVxC7689', 'album': 'great doubt',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2738c16c4c88eca4899d91be1b3',
                'preview_url': 'https://p.scdn.co/mp3-preview/7b816ba06521b3036b754ec7cb24527fe5cc4804?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': '! mavis beacon', 'id': '5cg5NA88xpoJyBHwq0UXoZ', 'artists_name': 'saya gray',
                'artists_id': '4EnymklUyqZwvmHQGlRssl', 'album': 'qwerty ii',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273457bc4f2b01a5383fec25f3d',
                'preview_url': 'https://p.scdn.co/mp3-preview/082df85c57183c90775852a80864d66be4f2d4d0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'like i say (i runaway)', 'id': '2D3oVAd8nHrqJH8UAfvtTT', 'artists_name': 'nilüfer yanya',
                'artists_id': '09kXLeOXRyfNQMXRaDO4qA', 'album': 'like i say (i runaway)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2732950207c7653f141661d4025',
                'preview_url': 'https://p.scdn.co/mp3-preview/d5aac2dcc101175a58fa5b4dddcdca736ac00929?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'turtle neck man', 'id': '2zGCWKIqswOmQCAA0peLQC', 'artists_name': 'mount kimbie',
                'artists_id': '3NUtpWpGDoffm3RCGhSHtl', 'album': 'turtle neck man',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2739746b9a8462a13751dcfc2c7',
                'preview_url': 'https://p.scdn.co/mp3-preview/5686be0a097191d3dfb5ae3f80536d3373b60d6f?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'fleshless hand', 'id': '7AYGjJHNrsIuC0LxxvWtEv', 'artists_name': 'ml buch',
                'artists_id': '3NsSv8HchEwfa7bGkjb4ZC', 'album': 'suntub',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27386a8513fec7563a8a6584c84',
                'preview_url': 'https://p.scdn.co/mp3-preview/342a2f1071d46335a0659546d1718527bc414a0a?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'miss understood', 'id': '7emOUo5DMccU8cg5X4uG79', 'artists_name': 'headache',
                'artists_id': '1iX0eIvL5iHnaDny7BBtWH', 'album': 'miss understood',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273696d4405302ff4b95dad5c75',
                'preview_url': 'https://p.scdn.co/mp3-preview/a62945773ccd9d4fc6f4e416064b1e1dc72f4cf9?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'jour 3', 'id': '1RLMR4pVuuHEzn8mOe1U2s', 'artists_name': 'hildegard',
                'artists_id': '2Ffds2i0bCHVuLiJq6GqCC', 'album': 'hildegard',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2736dbf6069df95c7708393a187',
                'preview_url': 'https://p.scdn.co/mp3-preview/613ab2bafa65f706128bc81a710b118df5ccc418?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'baby desert nobody', 'id': '4Z8bQSzhFitFU4QxTiNyrl', 'artists_name': 'jam city',
                'artists_id': '4jEa9eTpzzkuDQ9JMr0LT3', 'album': 'pillowland',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c56e3ebe99996a7bebf3efdb',
                'preview_url': 'https://p.scdn.co/mp3-preview/86cbb559a9e8ca474ab02b8a4c9769d4532064d4?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'something in the room she moves', 'id': '4q1wNhAe6axDOjReaCmOA3',
                'artists_name': 'julia holter', 'artists_id': '0bsV0sUjnCuCTYOnNHQl3E',
                'album': 'something in the room she moves',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737ee214f262d96b1e5ab3232d',
                'preview_url': 'https://p.scdn.co/mp3-preview/0dac8665f8d6959265b202dc884ee9426cde8e17?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'break4love', 'id': '5LRFjZ3lyfo7tlDAPuiL7V', 'artists_name': 'hype williams',
                'artists_id': '3SMaI6j8ObewCWPQFwfvui', 'album': 'one nation',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733216009439b2f93f5ee741c5',
                'preview_url': 'https://p.scdn.co/mp3-preview/2c5f50312a851702d265340fbd32e942a5bdccbd?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'disengage', 'id': '5tmiYtfKvYvCvcirDfyJDb', 'artists_name': 'acopia',
                'artists_id': '276EHqxzrJ8QJKoluzYjFr', 'album': 'acopia',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a89b142690c8aa500e7f8882',
                'preview_url': 'https://p.scdn.co/mp3-preview/568f125eacaf108479d131524d6668f61fce4bdb?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'fall apart', 'id': '4dL0IByCuNLmydwMRFokIM', 'artists_name': 'discovery zone',
                'artists_id': '4Q3A7ukbHFR5xThu9hZDZt', 'album': 'remote control',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737507a5adb06f2936b86b0e20',
                'preview_url': 'https://p.scdn.co/mp3-preview/bde5ef98a66d37cfdd4d8f7b2017a10088ba48dc?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'in the front', 'id': '5TH7kcmgdMUDpUiinmZbDl', 'artists_name': 'vegyn',
                'artists_id': '5iUnvXddCpOrbWKm7QMr6o', 'album': 'the road to hell is paved with good intentions',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273713972bc8bb25ef21c39d448',
                'preview_url': 'https://p.scdn.co/mp3-preview/ad28e9e3b1383e9ad14a857f86f790857a351814?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'favourite', 'id': '7oG9qhZ0UaQEoUGJJVXh1U', 'artists_name': 'fontaines d.c.',
                'artists_id': '3SXwqSqAoBz9WCI9PDQzY6', 'album': 'favourite',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273e2364cc87c592b004960b5a5',
                'preview_url': 'https://p.scdn.co/mp3-preview/612f6712f5d4c51cf74ae578bb28cf899f9e8a48?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'blue liquid', 'id': '57MWPH5Ucu2OEDD5yhhL6X', 'artists_name': 'mount kimbie',
                'artists_id': '3NUtpWpGDoffm3RCGhSHtl', 'album': 'black stone / blue liquid',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27382d26688e6975adac0dfc6ea',
                'preview_url': 'https://p.scdn.co/mp3-preview/68982111371434ec3181b97a4659376daf4a0eed?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'lead existence', 'id': '5YiUph3jpcaJ8JHkzITUVb', 'artists_name': 'king krule',
                'artists_id': '4wyNyxs74Ux8UIDopNjIai', 'album': 'king krule',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733e02c0dcf729dc64ae7bece0',
                'preview_url': 'https://p.scdn.co/mp3-preview/61e32d8bb706b40eac66a8e05343cebdb3dbe8a0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'daydream', 'id': '2YTIRy9Xvp5y9IJ4kRflxa', 'artists_name': 'voice actor',
                'artists_id': '6PsuUa5ijopH2T8rVzHSZc', 'album': 'fake sleep',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273b39285c788e1a5a7ab6df008',
                'preview_url': 'https://p.scdn.co/mp3-preview/c3da03bb67285681b8606bb8e2bd86070a1d88a0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'jumzzz', 'id': '08oY9ACcDjDff7b0t4mbjE', 'artists_name': 'loukeman',
                'artists_id': '10JL2s5aUztzFyURrFrxtL', 'album': 'sd-2',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273d6aa1689ab75f77758eb5b3b',
                'preview_url': 'https://p.scdn.co/mp3-preview/dba0c31ae354486be86f60b0cb86b6a40846b2d6?cid=6e82327445994df88d17de8cd6608f19'},{'name': 'manna', 'id': '0NGCFZaKB4WgUooVaAW4l8', 'artists_name': 'babyfather',
                'artists_id': '3DmDJOQgrwlq8MxXGLeFvA', 'album': 'aug freestyle / manna',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27390acc689ef1a170f0e357ca1',
                'preview_url': 'https://p.scdn.co/mp3-preview/ac7369a071b43474697fe387958b0b3ac47a053d?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'loving furlong', 'id': '2s9j8TV8rqK73MxStehVTD', 'artists_name': 'bullion',
                'artists_id': '6vcPgFOkMWBoY6Ks6eMEWj', 'album': 'heaven is over',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c5a7a4e34c5e05e533c4184e',
                'preview_url': 'https://p.scdn.co/mp3-preview/f0b8f7c570541032569922afb1c5171844c8cedf?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'whaleshark', 'id': '3BsBD6gkwdutyI7RQP5Ea4', 'artists_name': 'king krule',
                'artists_id': '4wyNyxs74Ux8UIDopNjIai', 'album': 'shhhhhhh!',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2731fec7a0acee1454153dba5b5',
                'preview_url': 'https://p.scdn.co/mp3-preview/d1dbb22af6be3177eed64f6f1297b0d14600d2ba?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'annie, pick a flower.. (my house)', 'id': '72AeIPJXQxYgtOIcmSnvQo',
                'artists_name': 'saya gray', 'artists_id': '4EnymklUyqZwvmHQGlRssl',
                'album': 'annie, pick a flower.. (my house)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a396a8aa9c5d2e31b77440ac',
                'preview_url': 'https://p.scdn.co/mp3-preview/d7b31bcbe63a8b1e9e0da5528839edccaf222168?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': "it's nice to be alive", 'id': '2vVMA6goXUgJSKcnnQrgin', 'artists_name': 'vegyn',
                'artists_id': '5iUnvXddCpOrbWKm7QMr6o', 'album': 'only diamonds cut diamonds',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273de301906ddf37189b1998f16',
                'preview_url': 'https://p.scdn.co/mp3-preview/e7ef9631647776457e9c7145705384f460d29c4d?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'new star in the sky - demo 1', 'id': '0ty8rSBaDkNPWO8Ex4ifUO', 'artists_name': 'air',
                'artists_id': '1P6U1dCeHxPui5pIrGmndZ', 'album': 'moon safari rarities (25th anniversary edition)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c4027cea1ac0a27a6801f3cf',
                'preview_url': 'https://p.scdn.co/mp3-preview/c7e2632e1c4ecef0e1803a54b2c61a8da6dad245?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'treat each other right', 'id': '52GJf3163rfoCtjOvCe85K', 'artists_name': 'jamie xx',
                'artists_id': '7A0awCXkE1FtSU8B0qwOJQ', 'album': 'treat each other right',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27382d2f93d353c3c7d0828959c',
                'preview_url': 'https://p.scdn.co/mp3-preview/a518fdb34284daa9a2298fd5491d6cede24a3e01?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'staying here', 'id': '4gdM3XzcjeJQZPpMvuf9VF', 'artists_name': 'astrid sonne',
                'artists_id': '7qiyPneI60DzZmxVxC7689', 'album': 'great doubt',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2738c16c4c88eca4899d91be1b3',
                'preview_url': 'https://p.scdn.co/mp3-preview/7b816ba06521b3036b754ec7cb24527fe5cc4804?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': '! mavis beacon', 'id': '5cg5NA88xpoJyBHwq0UXoZ', 'artists_name': 'saya gray',
                'artists_id': '4EnymklUyqZwvmHQGlRssl', 'album': 'qwerty ii',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273457bc4f2b01a5383fec25f3d',
                'preview_url': 'https://p.scdn.co/mp3-preview/082df85c57183c90775852a80864d66be4f2d4d0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'like i say (i runaway)', 'id': '2D3oVAd8nHrqJH8UAfvtTT', 'artists_name': 'nilüfer yanya',
                'artists_id': '09kXLeOXRyfNQMXRaDO4qA', 'album': 'like i say (i runaway)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2732950207c7653f141661d4025',
                'preview_url': 'https://p.scdn.co/mp3-preview/d5aac2dcc101175a58fa5b4dddcdca736ac00929?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'turtle neck man', 'id': '2zGCWKIqswOmQCAA0peLQC', 'artists_name': 'mount kimbie',
                'artists_id': '3NUtpWpGDoffm3RCGhSHtl', 'album': 'turtle neck man',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2739746b9a8462a13751dcfc2c7',
                'preview_url': 'https://p.scdn.co/mp3-preview/5686be0a097191d3dfb5ae3f80536d3373b60d6f?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'fleshless hand', 'id': '7AYGjJHNrsIuC0LxxvWtEv', 'artists_name': 'ml buch',
                'artists_id': '3NsSv8HchEwfa7bGkjb4ZC', 'album': 'suntub',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27386a8513fec7563a8a6584c84',
                'preview_url': 'https://p.scdn.co/mp3-preview/342a2f1071d46335a0659546d1718527bc414a0a?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'miss understood', 'id': '7emOUo5DMccU8cg5X4uG79', 'artists_name': 'headache',
                'artists_id': '1iX0eIvL5iHnaDny7BBtWH', 'album': 'miss understood',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273696d4405302ff4b95dad5c75',
                'preview_url': 'https://p.scdn.co/mp3-preview/a62945773ccd9d4fc6f4e416064b1e1dc72f4cf9?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'jour 3', 'id': '1RLMR4pVuuHEzn8mOe1U2s', 'artists_name': 'hildegard',
                'artists_id': '2Ffds2i0bCHVuLiJq6GqCC', 'album': 'hildegard',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2736dbf6069df95c7708393a187',
                'preview_url': 'https://p.scdn.co/mp3-preview/613ab2bafa65f706128bc81a710b118df5ccc418?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'baby desert nobody', 'id': '4Z8bQSzhFitFU4QxTiNyrl', 'artists_name': 'jam city',
                'artists_id': '4jEa9eTpzzkuDQ9JMr0LT3', 'album': 'pillowland',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c56e3ebe99996a7bebf3efdb',
                'preview_url': 'https://p.scdn.co/mp3-preview/86cbb559a9e8ca474ab02b8a4c9769d4532064d4?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'something in the room she moves', 'id': '4q1wNhAe6axDOjReaCmOA3',
                'artists_name': 'julia holter', 'artists_id': '0bsV0sUjnCuCTYOnNHQl3E',
                'album': 'something in the room she moves',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737ee214f262d96b1e5ab3232d',
                'preview_url': 'https://p.scdn.co/mp3-preview/0dac8665f8d6959265b202dc884ee9426cde8e17?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'break4love', 'id': '5LRFjZ3lyfo7tlDAPuiL7V', 'artists_name': 'hype williams',
                'artists_id': '3SMaI6j8ObewCWPQFwfvui', 'album': 'one nation',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733216009439b2f93f5ee741c5',
                'preview_url': 'https://p.scdn.co/mp3-preview/2c5f50312a851702d265340fbd32e942a5bdccbd?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'disengage', 'id': '5tmiYtfKvYvCvcirDfyJDb', 'artists_name': 'acopia',
                'artists_id': '276EHqxzrJ8QJKoluzYjFr', 'album': 'acopia',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a89b142690c8aa500e7f8882',
                'preview_url': 'https://p.scdn.co/mp3-preview/568f125eacaf108479d131524d6668f61fce4bdb?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'fall apart', 'id': '4dL0IByCuNLmydwMRFokIM', 'artists_name': 'discovery zone',
                'artists_id': '4Q3A7ukbHFR5xThu9hZDZt', 'album': 'remote control',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737507a5adb06f2936b86b0e20',
                'preview_url': 'https://p.scdn.co/mp3-preview/bde5ef98a66d37cfdd4d8f7b2017a10088ba48dc?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'in the front', 'id': '5TH7kcmgdMUDpUiinmZbDl', 'artists_name': 'vegyn',
                'artists_id': '5iUnvXddCpOrbWKm7QMr6o', 'album': 'the road to hell is paved with good intentions',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273713972bc8bb25ef21c39d448',
                'preview_url': 'https://p.scdn.co/mp3-preview/ad28e9e3b1383e9ad14a857f86f790857a351814?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'favourite', 'id': '7oG9qhZ0UaQEoUGJJVXh1U', 'artists_name': 'fontaines d.c.',
                'artists_id': '3SXwqSqAoBz9WCI9PDQzY6', 'album': 'favourite',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273e2364cc87c592b004960b5a5',
                'preview_url': 'https://p.scdn.co/mp3-preview/612f6712f5d4c51cf74ae578bb28cf899f9e8a48?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'blue liquid', 'id': '57MWPH5Ucu2OEDD5yhhL6X', 'artists_name': 'mount kimbie',
                'artists_id': '3NUtpWpGDoffm3RCGhSHtl', 'album': 'black stone / blue liquid',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27382d26688e6975adac0dfc6ea',
                'preview_url': 'https://p.scdn.co/mp3-preview/68982111371434ec3181b97a4659376daf4a0eed?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'lead existence', 'id': '5YiUph3jpcaJ8JHkzITUVb', 'artists_name': 'king krule',
                'artists_id': '4wyNyxs74Ux8UIDopNjIai', 'album': 'king krule',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733e02c0dcf729dc64ae7bece0',
                'preview_url': 'https://p.scdn.co/mp3-preview/61e32d8bb706b40eac66a8e05343cebdb3dbe8a0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'daydream', 'id': '2YTIRy9Xvp5y9IJ4kRflxa', 'artists_name': 'voice actor',
                'artists_id': '6PsuUa5ijopH2T8rVzHSZc', 'album': 'fake sleep',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273b39285c788e1a5a7ab6df008',
                'preview_url': 'https://p.scdn.co/mp3-preview/c3da03bb67285681b8606bb8e2bd86070a1d88a0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'jumzzz', 'id': '08oY9ACcDjDff7b0t4mbjE', 'artists_name': 'loukeman',
                'artists_id': '10JL2s5aUztzFyURrFrxtL', 'album': 'sd-2',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273d6aa1689ab75f77758eb5b3b',
                'preview_url': 'https://p.scdn.co/mp3-preview/dba0c31ae354486be86f60b0cb86b6a40846b2d6?cid=6e82327445994df88d17de8cd6608f19'},{'name': 'manna', 'id': '0NGCFZaKB4WgUooVaAW4l8', 'artists_name': 'babyfather',
                'artists_id': '3DmDJOQgrwlq8MxXGLeFvA', 'album': 'aug freestyle / manna',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27390acc689ef1a170f0e357ca1',
                'preview_url': 'https://p.scdn.co/mp3-preview/ac7369a071b43474697fe387958b0b3ac47a053d?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'loving furlong', 'id': '2s9j8TV8rqK73MxStehVTD', 'artists_name': 'bullion',
                'artists_id': '6vcPgFOkMWBoY6Ks6eMEWj', 'album': 'heaven is over',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c5a7a4e34c5e05e533c4184e',
                'preview_url': 'https://p.scdn.co/mp3-preview/f0b8f7c570541032569922afb1c5171844c8cedf?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'whaleshark', 'id': '3BsBD6gkwdutyI7RQP5Ea4', 'artists_name': 'king krule',
                'artists_id': '4wyNyxs74Ux8UIDopNjIai', 'album': 'shhhhhhh!',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2731fec7a0acee1454153dba5b5',
                'preview_url': 'https://p.scdn.co/mp3-preview/d1dbb22af6be3177eed64f6f1297b0d14600d2ba?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'annie, pick a flower.. (my house)', 'id': '72AeIPJXQxYgtOIcmSnvQo',
                'artists_name': 'saya gray', 'artists_id': '4EnymklUyqZwvmHQGlRssl',
                'album': 'annie, pick a flower.. (my house)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a396a8aa9c5d2e31b77440ac',
                'preview_url': 'https://p.scdn.co/mp3-preview/d7b31bcbe63a8b1e9e0da5528839edccaf222168?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': "it's nice to be alive", 'id': '2vVMA6goXUgJSKcnnQrgin', 'artists_name': 'vegyn',
                'artists_id': '5iUnvXddCpOrbWKm7QMr6o', 'album': 'only diamonds cut diamonds',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273de301906ddf37189b1998f16',
                'preview_url': 'https://p.scdn.co/mp3-preview/e7ef9631647776457e9c7145705384f460d29c4d?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'new star in the sky - demo 1', 'id': '0ty8rSBaDkNPWO8Ex4ifUO', 'artists_name': 'air',
                'artists_id': '1P6U1dCeHxPui5pIrGmndZ', 'album': 'moon safari rarities (25th anniversary edition)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c4027cea1ac0a27a6801f3cf',
                'preview_url': 'https://p.scdn.co/mp3-preview/c7e2632e1c4ecef0e1803a54b2c61a8da6dad245?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'treat each other right', 'id': '52GJf3163rfoCtjOvCe85K', 'artists_name': 'jamie xx',
                'artists_id': '7A0awCXkE1FtSU8B0qwOJQ', 'album': 'treat each other right',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27382d2f93d353c3c7d0828959c',
                'preview_url': 'https://p.scdn.co/mp3-preview/a518fdb34284daa9a2298fd5491d6cede24a3e01?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'staying here', 'id': '4gdM3XzcjeJQZPpMvuf9VF', 'artists_name': 'astrid sonne',
                'artists_id': '7qiyPneI60DzZmxVxC7689', 'album': 'great doubt',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2738c16c4c88eca4899d91be1b3',
                'preview_url': 'https://p.scdn.co/mp3-preview/7b816ba06521b3036b754ec7cb24527fe5cc4804?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': '! mavis beacon', 'id': '5cg5NA88xpoJyBHwq0UXoZ', 'artists_name': 'saya gray',
                'artists_id': '4EnymklUyqZwvmHQGlRssl', 'album': 'qwerty ii',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273457bc4f2b01a5383fec25f3d',
                'preview_url': 'https://p.scdn.co/mp3-preview/082df85c57183c90775852a80864d66be4f2d4d0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'like i say (i runaway)', 'id': '2D3oVAd8nHrqJH8UAfvtTT', 'artists_name': 'nilüfer yanya',
                'artists_id': '09kXLeOXRyfNQMXRaDO4qA', 'album': 'like i say (i runaway)',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2732950207c7653f141661d4025',
                'preview_url': 'https://p.scdn.co/mp3-preview/d5aac2dcc101175a58fa5b4dddcdca736ac00929?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'turtle neck man', 'id': '2zGCWKIqswOmQCAA0peLQC', 'artists_name': 'mount kimbie',
                'artists_id': '3NUtpWpGDoffm3RCGhSHtl', 'album': 'turtle neck man',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2739746b9a8462a13751dcfc2c7',
                'preview_url': 'https://p.scdn.co/mp3-preview/5686be0a097191d3dfb5ae3f80536d3373b60d6f?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'fleshless hand', 'id': '7AYGjJHNrsIuC0LxxvWtEv', 'artists_name': 'ml buch',
                'artists_id': '3NsSv8HchEwfa7bGkjb4ZC', 'album': 'suntub',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27386a8513fec7563a8a6584c84',
                'preview_url': 'https://p.scdn.co/mp3-preview/342a2f1071d46335a0659546d1718527bc414a0a?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'miss understood', 'id': '7emOUo5DMccU8cg5X4uG79', 'artists_name': 'headache',
                'artists_id': '1iX0eIvL5iHnaDny7BBtWH', 'album': 'miss understood',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273696d4405302ff4b95dad5c75',
                'preview_url': 'https://p.scdn.co/mp3-preview/a62945773ccd9d4fc6f4e416064b1e1dc72f4cf9?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'jour 3', 'id': '1RLMR4pVuuHEzn8mOe1U2s', 'artists_name': 'hildegard',
                'artists_id': '2Ffds2i0bCHVuLiJq6GqCC', 'album': 'hildegard',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2736dbf6069df95c7708393a187',
                'preview_url': 'https://p.scdn.co/mp3-preview/613ab2bafa65f706128bc81a710b118df5ccc418?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'baby desert nobody', 'id': '4Z8bQSzhFitFU4QxTiNyrl', 'artists_name': 'jam city',
                'artists_id': '4jEa9eTpzzkuDQ9JMr0LT3', 'album': 'pillowland',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c56e3ebe99996a7bebf3efdb',
                'preview_url': 'https://p.scdn.co/mp3-preview/86cbb559a9e8ca474ab02b8a4c9769d4532064d4?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'something in the room she moves', 'id': '4q1wNhAe6axDOjReaCmOA3',
                'artists_name': 'julia holter', 'artists_id': '0bsV0sUjnCuCTYOnNHQl3E',
                'album': 'something in the room she moves',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737ee214f262d96b1e5ab3232d',
                'preview_url': 'https://p.scdn.co/mp3-preview/0dac8665f8d6959265b202dc884ee9426cde8e17?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'break4love', 'id': '5LRFjZ3lyfo7tlDAPuiL7V', 'artists_name': 'hype williams',
                'artists_id': '3SMaI6j8ObewCWPQFwfvui', 'album': 'one nation',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733216009439b2f93f5ee741c5',
                'preview_url': 'https://p.scdn.co/mp3-preview/2c5f50312a851702d265340fbd32e942a5bdccbd?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'disengage', 'id': '5tmiYtfKvYvCvcirDfyJDb', 'artists_name': 'acopia',
                'artists_id': '276EHqxzrJ8QJKoluzYjFr', 'album': 'acopia',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a89b142690c8aa500e7f8882',
                'preview_url': 'https://p.scdn.co/mp3-preview/568f125eacaf108479d131524d6668f61fce4bdb?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'fall apart', 'id': '4dL0IByCuNLmydwMRFokIM', 'artists_name': 'discovery zone',
                'artists_id': '4Q3A7ukbHFR5xThu9hZDZt', 'album': 'remote control',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737507a5adb06f2936b86b0e20',
                'preview_url': 'https://p.scdn.co/mp3-preview/bde5ef98a66d37cfdd4d8f7b2017a10088ba48dc?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'in the front', 'id': '5TH7kcmgdMUDpUiinmZbDl', 'artists_name': 'vegyn',
                'artists_id': '5iUnvXddCpOrbWKm7QMr6o', 'album': 'the road to hell is paved with good intentions',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273713972bc8bb25ef21c39d448',
                'preview_url': 'https://p.scdn.co/mp3-preview/ad28e9e3b1383e9ad14a857f86f790857a351814?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'favourite', 'id': '7oG9qhZ0UaQEoUGJJVXh1U', 'artists_name': 'fontaines d.c.',
                'artists_id': '3SXwqSqAoBz9WCI9PDQzY6', 'album': 'favourite',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273e2364cc87c592b004960b5a5',
                'preview_url': 'https://p.scdn.co/mp3-preview/612f6712f5d4c51cf74ae578bb28cf899f9e8a48?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'blue liquid', 'id': '57MWPH5Ucu2OEDD5yhhL6X', 'artists_name': 'mount kimbie',
                'artists_id': '3NUtpWpGDoffm3RCGhSHtl', 'album': 'black stone / blue liquid',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27382d26688e6975adac0dfc6ea',
                'preview_url': 'https://p.scdn.co/mp3-preview/68982111371434ec3181b97a4659376daf4a0eed?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'lead existence', 'id': '5YiUph3jpcaJ8JHkzITUVb', 'artists_name': 'king krule',
                'artists_id': '4wyNyxs74Ux8UIDopNjIai', 'album': 'king krule',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733e02c0dcf729dc64ae7bece0',
                'preview_url': 'https://p.scdn.co/mp3-preview/61e32d8bb706b40eac66a8e05343cebdb3dbe8a0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'daydream', 'id': '2YTIRy9Xvp5y9IJ4kRflxa', 'artists_name': 'voice actor',
                'artists_id': '6PsuUa5ijopH2T8rVzHSZc', 'album': 'fake sleep',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273b39285c788e1a5a7ab6df008',
                'preview_url': 'https://p.scdn.co/mp3-preview/c3da03bb67285681b8606bb8e2bd86070a1d88a0?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'jumzzz', 'id': '08oY9ACcDjDff7b0t4mbjE', 'artists_name': 'loukeman',
                'artists_id': '10JL2s5aUztzFyURrFrxtL', 'album': 'sd-2',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273d6aa1689ab75f77758eb5b3b',
                'preview_url': 'https://p.scdn.co/mp3-preview/dba0c31ae354486be86f60b0cb86b6a40846b2d6?cid=6e82327445994df88d17de8cd6608f19'}]
=======
tracks_list = [{'name': 'pyramids', 'id': '4QhWbupniDd44EDtnh2bFJ', 'artists_name': 'frank ocean',
                'artists_id': '2h93pZq0e7k5yf4dywlkpM', 'album_name': 'channel orange',
                'album_id': '392p3shh2jkxUxY2VHvlH8',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737aede4855f6d0d738012e2e5',
                'preview_url': 'https://p.scdn.co/mp3-preview/0fff01329318a30ba0b7c2a872c0113e6742a364'},
               {'name': 'sweater weather', 'id': '2QjOHCTQ1Jl3zawyYOpxh6', 'artists_name': 'the neighbourhood',
                'artists_id': '77SW9BnxLY8rJ0RciFqkHh', 'album_name': 'i love you.',
                'album_id': '4xkM0BwLM9H2IUcbYzpcBI',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2738265a736a1eb838ad5a0b921',
                'preview_url': 'https://p.scdn.co/mp3-preview/877602f424a9dea277b13301ffc516f9fd1fbe7e?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'leray', 'id': '3sitsgJXmK6cKT0XkfXuJ9', 'artists_name': 'trippie redd',
                'artists_id': '6Xgp2XMz1fhVYe7i6yNAax', 'album_name': 'a love letter to you 4',
                'album_id': '5nDqjtvRwDYElIflvoNDdE',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273338fabbb1729a74d655a6a85',
                'preview_url': 'https://p.scdn.co/mp3-preview/9a3b1f1ac72e123ded0022772011aff1a3f6f4ea?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'cinnamon girl', 'id': '2mdEsXPu8ZmkHRRtAdC09e', 'artists_name': 'lana del rey',
                'artists_id': '00FQb4jTyendYWaN8pK0wa', 'album_name': 'norman fucking rockwell!',
                'album_id': '5XpEKORZ4y6OrCZSKsi46A',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273879e9318cb9f4e05ee552ac9',
                'preview_url': 'https://p.scdn.co/mp3-preview/e77692e884a30ed4d1ce3df27e408066e37c315b'},
               {'name': 'pretty girl', 'id': '0KyAGiNGUytG5JLxJu4F6l', 'artists_name': 'clairo',
                'artists_id': '3l0CmX0FuQjFxr8SK7Vqag', 'album_name': 'pretty girl',
                'album_id': '3nkwKrSQJ9l84VV8uuymk9',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273efe812ae54f0698a32ccae14',
                'preview_url': 'https://p.scdn.co/mp3-preview/9dfa6eaf9492ac2bf1cb507b69a1792ad7850328'},
               {'name': 'superpowers', 'id': '736PP5LTtREkDgktNmX3Gu', 'artists_name': 'daniel caesar',
                'artists_id': '20wkVLutqVOYrc0kxFs7rA', 'album_name': 'never enough',
                'album_id': '7ivbFszr1TbVadj89BIy1y',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737c68face1dc58127f3a7b1cc',
                'preview_url': 'https://p.scdn.co/mp3-preview/33c4b7ce820311cdd299d86bbfeb7b688cefe529'},
               {'name': 'mary', 'id': '4p9iQNEmsIGkB6eG8Val8n', 'artists_name': 'alex g',
                'artists_id': '6lcwlkAjBPSKnFBZjjZFJs', 'album_name': 'trick', 'album_id': '2Vg8YkTkuG4Y9MD4hB4KNN',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2734214b89510fae59a643aa1b2',
                'preview_url': 'https://p.scdn.co/mp3-preview/d1396c2f354d0bd484146b0bb387746a509f0184?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'reborn', 'id': '4RVbK6cV0VqWdpCDcx3hiT', 'artists_name': 'kids see ghosts',
                'artists_id': '2hPgGN4uhvXAxiXQBIXOmE', 'album_name': 'kids see ghosts',
                'album_id': '6pwuKxMUkNg673KETsXPUV',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273013c00ee367dd85396f79c82',
                'preview_url': 'https://p.scdn.co/mp3-preview/f75ac65c50fcc81e642f58220e7f3abaf827e77a'},
               {'name': 'your teeth in my neck', 'id': '54IbnYEdA3ymfxv07WgN3b', 'artists_name': 'kali uchis',
                'artists_id': '1U1el3k54VvEUzo3ybLPlM', 'album_name': 'isolation', 'album_id': '4EPQtdq6vvwxuYeQTrwDVY',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b27390b4e1905b1fc48c537ec053',
                'preview_url': 'https://p.scdn.co/mp3-preview/7b3f7e9d854a3dfc22b79f07909031bfe257ef54'},
               {'name': 'anything', 'id': '4PwWESSlTwzvw9B7bmtTLS', 'artists_name': 'adrianne lenker',
                'artists_id': '4aKWmkWAKviFlyvHYPTNQY', 'album_name': 'songs', 'album_id': '2Qt8Z1LB3Fsrf6nhBNsvUJ',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273ab009ce861613653b14451b9',
                'preview_url': 'https://p.scdn.co/mp3-preview/e2d939054c9d00c2d5a63619daa6f787c05cef2a?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'all the stars (with sza)', 'id': '3GCdLUSnKSMJhs4Tj6CV3s', 'artists_name': 'kendrick lamar',
                'artists_id': '2YZyLoL8N0Wb9xBt1NhZWg',
                'album_name': 'black panther the album music from and inspired by',
                'album_id': '3pLdWdkj83EYfDN6H2N8MR',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c027ad28821777b00dcaa888',
                'preview_url': 'https://p.scdn.co/mp3-preview/330c6d6e5bfcc1bc831b6948b57ce9c98e7558bf'},
               {'name': 'sex, drugs, etc.', 'id': '7MlDNspYwfqnHxORufupwq', 'artists_name': 'beach weather',
                'artists_id': '7I3bkknknQkIiatWiupQgD', 'album_name': 'pineapple sunrise',
                'album_id': '7gA8QSNSZvHUYC9feFpeLj',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a03e3d24ccee1c370899c342',
                'preview_url': 'https://p.scdn.co/mp3-preview/a423aecddb590788a61f2a7b4d325bf461f88dc8?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'no role modelz', 'id': '68Dni7IE4VyPkTOH9mRWHr', 'artists_name': 'j. cole',
                'artists_id': '6l3HvQ5sa6mXTsMTB19rO5', 'album_name': '2014 forest hills drive',
                'album_id': '0UMMIkurRUmkruZ3KGBLtG',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273c6e0948bbb0681ff29cdbae8',
                'preview_url': 'https://p.scdn.co/mp3-preview/062b69c85ad8361d6d7e484aa798b3596d174306'},
               {'name': 'pretty little fears (feat. j. cole)', 'id': '4at3d5QWnlibMVN75ECDrp', 'artists_name': '6lack',
                'artists_id': '4IVAbR2w4JJNJDDRFP3E83', 'album_name': 'east atlanta love letter',
                'album_id': '3fc97ZWLIMc1xawhxbKrh2',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273e1530b42603367fdb2208d88',
                'preview_url': 'https://p.scdn.co/mp3-preview/4bda22e1bb78bc7a0d1d9e87bc35fa2dd6648f5b'},
               {'name': "could've been (feat. bryson tiller)", 'id': '6oEVnWKgPqIEPc53OYDNqG', 'artists_name': 'h.e.r.',
                'artists_id': '3Y7RZ31TRPVadSFVy1o8os', 'album_name': 'i used to know her',
                'album_id': '0IMTA2Wz6p8CNZ0MDK2zvg',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2732066a381ebbbb1f8312764e7',
                'preview_url': 'https://p.scdn.co/mp3-preview/3ea3f13a61edf4fe0ab2fee73669a14dd3d257d7?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'chanel', 'id': '6Nle9hKrkL1wQpwNfEkxjh', 'artists_name': 'frank ocean',
                'artists_id': '2h93pZq0e7k5yf4dywlkpM', 'album_name': 'chanel', 'album_id': '6OGzmhzHcjf0uN9j7dYvZH',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273a0b780c23fc3c19bd412b234',
                'preview_url': 'https://p.scdn.co/mp3-preview/0eb4e74aaf59feacf5bc4edeaf5e03360eb86385?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'ball w/o you', 'id': '50a8bKqlwDEqeiEknrzkTO', 'artists_name': '21 savage',
                'artists_id': '1URnnhqYAYcrqrcwql10ft', 'album_name': 'i am > i was',
                'album_id': '007DWn799UWvfY1wwZeENR',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b273280689ecc5e4b2038bb5e4bd',
                'preview_url': 'https://p.scdn.co/mp3-preview/29092f27b687647064cb116289ac78ab2c4a2118?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'sunshine (feat. fousheé)', 'id': '14Q7Qja4PJwjMsKdBZcnww', 'artists_name': 'steve lacy',
                'artists_id': '57vWImR43h4CaDao012Ofp', 'album_name': 'gemini rights',
                'album_id': '4tRInpsZkScWnp3UWcdLTq',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2735cc2b8beee1bae039987f2d2',
                'preview_url': 'https://p.scdn.co/mp3-preview/179b889e9623486dde26f16180ebec91bd8d51fd?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'lady killers ii', 'id': '1xUddpWyEuYl5T3mduKnOJ', 'artists_name': 'g-eazy',
                'artists_id': '02kJSzxNuaWGqwubyUba0Z', 'album_name': 'lady killers ii',
                'album_id': '08JECZoQNpeSledQtNZp6H',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2733e20c68adf6bc6e0e5f40b3d',
                'preview_url': 'https://p.scdn.co/mp3-preview/fe9af50aabaa91970d74b9bcb404af661d234b36?cid=6e82327445994df88d17de8cd6608f19'},
               {'name': 'crew (feat. brent faiyaz & shy glizzy)', 'id': '15EPc80XuFrb2LmOzGjuRg',
                'artists_name': 'goldlink', 'artists_id': '5XenQ7XfcvQdfIbpLEFaKQ', 'album_name': 'at what cost',
                'album_id': '18JrBX1QkpnUSJF3oxX6RX',
                'album_cover': 'https://i.scdn.co/image/ab67616d0000b2737bcd3cd54e8399ae38cc6e64',
                'preview_url': 'https://p.scdn.co/mp3-preview/43bbfb0a4ff1ce6999b044d67d513aac7273e5ee?cid=6e82327445994df88d17de8cd6608f19'}]
>>>>>>> 1ebd5496d4664646c5b43dd27abbbfb1b1e97748


@main_bp.route('/')
def home():
    tracks_data = db.session.query(user_track).all()
    recently_liked_tracks = tracks_data[-5:]
    recently_liked_track_ids = [track[1] for track in reversed(recently_liked_tracks)]

    track_ids = [track[1] for track in tracks_data]
    tracks = Track.query.filter(Track.id.in_(recently_liked_track_ids)).all()
    tracks_for_genres = Track.query.filter(Track.id.in_(track_ids)).all()
    print(tracks)

    genres_like_count = Counter()
    for track in tracks_for_genres:
        genres = track.genres.split('.')
        genres_like_count.update(genres)
    popular_genres = dict(genres_like_count.most_common()[:10])

    artists_data = db.session.query(user_artist).all()
    artist_ids = [artist[1] for artist in artists_data]
    artist_like_count = Counter(artist_ids)

    popular_artists = [artist_id for artist_id, _ in artist_like_count.most_common()]
    artists = Artist.query.filter(Artist.id.in_(popular_artists)).all()
    artist_dict = {artist.id: artist for artist in artists}

    artist_data_list = []
    for artist_id in popular_artists:
        artist = artist_dict[artist_id]
        artist_data_list.append({
            'id': artist_id,
            'name': artist.name,
            'image': artist.image,
        })

    albums_data = db.session.query(user_album).all()
    album_ids = [album[1] for album in albums_data]
    album_like_count = Counter(album_ids)

    popular_albums = [album_id for album_id, _ in album_like_count.most_common()]
    albums = Album.query.filter(Album.id.in_(popular_albums)).all()
    album_dict = {album.id: album for album in albums}

    album_data_list = []
    for album_id in popular_albums:
        album = album_dict[album_id]
        album_data_list.append({
            'id': album_id,
            'name': album.name,
            'cover': album.cover,
        })
    return render_template('main/home.html', recently_liked_tracks=tracks, artists=artists, albums=albums,
                           genres=popular_genres)


@main_bp.route('/recommendations')
@login_required
@token_required
def recommendations():
    # genres = {}
    # seed_tracks = []
    # for track in current_user.tracks:
    #     track_genres = str(track.genres).split('.')
    #     for genre in track_genres:
    #         if genre not in genres:
    #             genres[genre] = []
    #         genres[genre].append(track.id)
    # if 'genres_list' not in session:
    #     session['genres_list'] = list(genres.keys())
    # genres_list = session['genres_list']
    # if not genres_list:
    #     genres_list = list(genres.keys())
    # for _ in range(len(genres_list[:5])):
    #     random_genre = choice(genres_list)
    #     print(random_genre)
    #     genre_songs = genres[random_genre]
    #     track_id = choice(genre_songs)
    #     seed_tracks.append(track_id)
    #     genres_list.remove(random_genre)
    # session['genres_list'] = genres_list
    # # janrebi
    # # example_choice = ['art pop', 'jazz fusion', 'experimental']
    # # for genre in example_choice:
    # #     tracks = Track.query.filter(Track.genres.contains(genre)).all()
    # #     for track in tracks:
    # #         if genre not in genres:
    # #             genres[genre] = []
    # #         genres[genre].append(track.name)
    # # for _ in range(len(example_choice)):
    # #     random_genre = choice(example_choice)
    # #     genre_songs = genres[random_genre]
    # #     track_id = choice(genre_songs)
    # #     seed_tracks.append(track_id)
    # #     example_choice.remove(random_genre)
    # # seed_tracks = ','.join(seed_tracks)
    # # print(seed_tracks)
    # # -------
    # headers = {
    #     "Authorization": f"Bearer {session['access_token']}"
    # }
    # params = {
    #     'limit': 20,
    #     'market': 'US',
    #     'seed_tracks': seed_tracks,
    # }
    #
    # response = requests.get(f'https://api.spotify.com/v1/recommendations?', headers=headers, params=params)
    # if 'tracks' not in session:
    #     session['tracks'] = []
    # tracks = []
    # liked_tracks = {track.id for track in current_user.tracks}
    # session_tracks = set(session['tracks'])
    # for n in range(len(response.json()['tracks'])):
    #     track = response.json()['tracks'][n]
    #     track_id = track['id']
    #     if track_id not in liked_tracks and track_id not in session_tracks:
    #         track_body = {
    #             'name': track['name'].lower(),
    #             'id': track_id,
    #             'artists_name': track['artists'][0]['name'].lower(),
    #             'artists_id': track['artists'][0]['id'],
    #             'album_name': track['album']['name'].lower(),
    #             'album_id': track['album']['id'],
    #             'album_cover': track['album']['images'][0]['url'],
    #             'preview_url': track.get('preview_url') or get_preview_url_if_null(track_id),
    #         }
    #         tracks.append(track_body)
    #         session['tracks'].append(track_id)
    return render_template('main/recommendations.html', tracks=tracks_list)


@main_bp.route('/dlt')
def dlt():
    print(len(session['tracks']))
    del session['tracks']
    return ''
