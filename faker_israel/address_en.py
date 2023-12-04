from faker.providers.address.he_IL import Provider as BaseHeAddressProvider


class AddressEnProvider(BaseHeAddressProvider):
    street_titles = list(set([s.strip() for s in '''
        Aviv
        Avigail
        Even Mas'ud
        Abrabanel
        Avraham Barzilai
        Egoz
        Admon
        Aharon Meir Mazia
        Ahronovitz
        Ulpan
        Oranim
        Azor Bet HaKvarot
        Azor Ta'asiya Aleph
        Azor Ta'asiya Har Yona
        Azor Ta'asiya
        Azor Ta'asiya Mizrach
        Achi Eilat
        Izaak Newton
        Iyar
        Ilania
        Imber
        Iros
        Iros
        Alverod
        Elul
        Aluma
        Elzabod
        Al-Zahra
        Elisher
        Alkanesset
        Alexander Yannai
        Elkharum
        Alkhtab
        Al-Limon
        Almazdlafeh
        Alslilmeh
        Alsaris
        Al'emshakah
        Al'akabah
        Alpf'jar
        Alrashid
        Alten
        Alterman
        Asa HaMelech
        Apeal
        Arbel
        Ashdod
        Eshel
        Etgar
        Ater Hafetz Hayim
        Boaz
        Bursat HaYahalomim
        Bikurim
        Bilu
        Bilinson
        Beit Avot
        Beit Hayotzer
        Beit Yitzhak-Sha'ar Hefer
        Beit Rishon BeMoladet
        Ben Yehuda
        Ben Yishai
        Ben Lebert
        Ben Tzvi Yitzhak
        Ben Tzvi Shimon
        Beka'at Hayareach
        Bergman Eliezer
        Bruriah
        Brazil
        Bareket
        Bashamat
        Bashamat
        Giva
        Giva
        Gober Rivkah
        Gotmakher
        Golda Meir
        Jo Amar
        Gibaton Hanoch
        Ginosar
        Gefen
        Gefen
        Gertrude Kraus
        Greenboim
        Devorah
        Dudu Dotan
        Dolav
        Dolchin Aryeh
        Dachy
        Diah
        Dimitar Peshov
        Darb Albarag'
        Deromit-Majd Alkharum
        Dreyfus
        Derekh Haaretz
        Derekh Hagan
        Derekh Hevron
        Derekh Chalamit
        Ha'odem
        Ha'oren
        Ha'ornim
        Ha'achim Bezharno
        Ha'elan
        Ha'ilanot
        Ha'ilit
        Ha'alonim
        Ha'amoraim
        Ha'etzadyon
        Ha'etzl
        Habardalas
        Habarosh
        Habrigada
        Hagevurah
        Hagefen
        Hagefen
        Hadaganot
        Hadolev
        Hadayagim
        Hahagana
        Holtsberg Simha
        Hofert Yaakov
        Hordim
        Horkanus Yochanan
        Hazaytim
        Hazamir
        Hachavel
        Hachoterim
        Hachalutzim
        Hachalil
        Hachamnit
        Hachasidah
        Hachatzav
        Hachatzav
        Hacharuv
        Hacharuvim
        Hacharmon
        Hachashmal
        Hayozem
        Hayanshuf
        Hayakinton
        Hala'h
        Hamea Ve'ahad
        Hambri'a
        Hambrek
        Hamagenim
        Hamagenim
        Hamored
        Hamayesdim
        Hamelacha
        Hamelacha
        Hamelachim
        Hamemuneh
        Hamenora
        Hamesger
        Hamaayan
        Hamafrash
        Hametzuda
        Hamarganit
        Hamashor
        Hanoter
        Hanurit
        Hanurit
        Hanekar
        Hanerd
        Hasiglit
        Hasifon
        Ha'avoda
        Ha'avoda
        Ha'atzmon
        Hapa'amon
        Hapardes
        Hapardes
        Hapardes
        Hapardes
        Hatza'alon
        Hatzab'onui
        Hakishon
        Harishonim
        Harav Bidani Ovadya
        Harav Wolff
        Harav Hakham Shimon
        Harabi Miliubavitch
        Harav Nissim
        Harav Uziel
        Harav Rafael Avu
        Hardof
        Hardof
        Hardof
        Harotem
        Harey Golan
        Har Yehal
        Harimon
        Har Kna'an
        Harlitz Yosef
        Har Sinai
        Har Atzmon
        Har Tzror
        Harkafot
        Harshko Avraham
        Harashet
        Hasadot
        Hashachar
        Hashizaf
        Hashiach
        Hashitah
        Hasha'ora
        Hashar Barzilai
        Hate'ena
        Hatavor
        Hatikvah
        Viktor VeYulius
        Va'eret Sa'ad
        Zhabotinsky
        Zaggai
        Zigurd
        Ziv
        Zhilber
        Zayit
    '''.split() if s.strip()]))

    city_names = list(set([s.strip() for s in '''
        Zikhron Ya'akov
        Huchit
        Hof Hayam
        Choshen
        Chazon Ish
        Hazan Yaakov
        Chitah
        Chaim Weitzman
        Chalmish
        Chatzav
        Charat A Bus
        Chatukha Yoram
        Taabliya
        Taachonot Alrahib
        Tabiv
        Topaz
        Ya B'Adar
        Yafa
        Yad Haapala Mimaroko
        Yedida
        Yehuda Halevi
        Yehuda Hamaccabi
        Yehuda Hamaccabi
        Yoav
        Yona
        Yizre'el
        Yehezkel Hanavi
        Yakhin
        Yerushalayim
        Yarkon
        Yeshu'at David
        Yissachar
        Kabul
        Kohen Eli
        Kahana
        Kokhav Hatsefon
        Kaziv
        Kisufim
        Kikar Yarden
        Kikar Nahshon
        Kinneret
        Kfar Yeladim Nirdim
        Kerem Chemed
        Lev Hakeirya
        Lavi Arik
        Levkovitz
        Lod Hazeira
        Lotem
        Levin Michael VeHannah
        Levin Shmaryahu
        Luria
        Lechi
        Lilienblum
        Lachish
        Leskov Chaim
        Mavo Hadas
        Mavo Hazaytim
        Mavo Chaim Makovna
        Mavo Chama
        Mivtza Harel
        Mivtza Hiram
        Mivtza Oveda
        Magellan
        Mosyof Shlomo
        Mofak Diab
        Moza
        Mordei Hagetaot
        Moran
        Mazal Shor
        Mizrachi Yosef
        Micha
        Meron
        Misha'el
        Malon Royal Park
        Menzar Hamaaronim
        Ma'avar Layam
        Maoz Chaim
        Maeonot Yam
        Ma'aleh
    '''.split() if s.strip()]))
