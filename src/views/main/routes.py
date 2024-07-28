import requests
from random import choice
from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from collections import Counter

from src.extensions import db
from src.models.models import Track, Artist, Album, user_artist, user_album, user_track
from src.functions import get_preview_url_if_null, token_required

main_bp = Blueprint('main', __name__)

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
    return render_template('main/home.html', recently_liked_tracks=tracks, artists=artists, albums=albums, genres=popular_genres)


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
    # janrebi
    # example_choice = ['art pop', 'jazz fusion', 'experimental']
    # for genre in example_choice:
    #     tracks = Track.query.filter(Track.genres.contains(genre)).all()
    #     for track in tracks:
    #         if genre not in genres:
    #             genres[genre] = []
    #         genres[genre].append(track.name)
    # for _ in range(len(example_choice)):
    #     random_genre = choice(example_choice)
    #     genre_songs = genres[random_genre]
    #     track_id = choice(genre_songs)
    #     seed_tracks.append(track_id)
    #     example_choice.remove(random_genre)
    # seed_tracks = ','.join(seed_tracks)
    # print(seed_tracks)
    # -------
    # headers = {
    #     "Authorization": f"Bearer {session['access_token']}"
    # }
    # params = {
    #     'limit': 20,
    #     'market': 'US',
    #     'seed_tracks': seed_tracks,
    # }
    #
    # response = requests.get(src'https://api.spotify.com/v1/recommendations?', headers=headers, params=params)
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
