from textwrap import dedent

from .salary import Salary, _, common_draw


class SalaryNorth(Salary):

    def __init__(self, *args, **kwargs):
        kwargs['no_bg'] = False
        super().__init__(*args, **kwargs)
        self.default_label = {
            "font": "Arial", "font_size": 10
        }
        fake = self.provider.generator
        company = fake.company()
        street_address = fake.street_address()
        city = fake.city()
        header_top_line = f"{company}, {street_address}, {city}"
        rashut = fake.random_element(["58", "42"])
        tik_nikuim = fake.numerify("#########")
        tik_bl = f'{tik_nikuim}00'
        self.labels = {
            "HeaderBox": {
                "border_color": "#cccccc",
                # "line_height": 14,
                "x_offset": -6, 'y_offset': -5,
                'html': dedent(f'''
                    <b>Hello</b>, World!
                ''').strip(),
                # "multiline_text_segments": [
                #     header_top_line,
                #     [
                #         "רשות:",
                #         {"text": str(rashut), "font": "Arial_Bold", "font_size": 10},
                #         "   ",
                #         "תיק ניכויים: ",
                #         {"text": str(tik_nikuim), "font": "Arial_Bold", "font_size": 10},
                #     ],
                #     [
                #         {"text": "רשות:", "color": ""},
                #         {"text": str(rashut), "font": "Arial_Bold", "font_size": 10, "color": ""},
                #         "   ",
                #         "ח-פ: ",
                #         {"text": "", "font": "Arial_Bold", "font_size": 10},
                #     ],
                #     [
                #         {"text": "רשות:", "color": ""},
                #         {"text": str(rashut), "font": "Arial_Bold", "font_size": 10, "color": ""},
                #         "   ",
                #         "תיק ב\"ל: ", "    ",
                #         {"text": str(tik_bl), "font": "Arial_Bold", "font_size": 10},
                #     ],
                # ],
            },
            "HeaderDepartment": {
                "text": "FOOBAR"
            }
            # HeaderLogo
            # AddressBoxTop
            # AddressBottomBox
            # DataMisraPlusTashlumim
            # DataNikuimIshiimPlusHova
            # DataNetoPayment
            # DataNikuiReshut
            # DataBoxNetuneiMisra
            # DataSahachSacharBasis
            # DataBoxNetunimNosafim
            # DataBoxTosafotPensionionLabasis
            # DataSahachSacharKoveaLepensia
            # DataBoxHehzerHotzaot
            # DataSahachHezerHotzaot
            # DataBoxTashlumimNosafim
            # DataSahachTashlumimNosafim
            # DataBoxRehiveiAvodaNosefet
            # DataSahachRehiveiAvodaNosefet
            # DataBoxPerutVetakimNosafim
            # DataBoxPirteyHeshbonBank
            # DataBoxMasHachnasaMonths
            # DataHodsheiAvoda
            # DataYehidotMas
            # DataNekudotZikui
            # DataAhuzShuli
            # DataHetMakorHizoni
            # DataYodMasHizoni
            # DataBoxTaarifimIshiimVeKlaliim
            # DataSacharRagil
            # DataHefreshim
            # DataHafrashaHayevet
            # DataPtorMasDmeiTipul
            # DataErechNekudotZikui
            # DataBoxShoviLemas
            # DataSahachShoviLemas
            # FooterCompanyName
            # FooterCompanyLogo
            # FooterCompanyDomain
        }

    def save(self, path, **kwargs):
        draw, draw_labels, image = self.save_init(
            path,
            'salaries/north',
            lambda item: item.get('value', {}).get('choices', [None]).pop() == _('North'),
            self.labels,
            self.default_label
        )
        with common_draw.init_html_page() as html_page:
            for label_id, label in draw_labels.items():
                # print(label_id, label)
                common_draw.draw_textbox(draw, **label, no_bg=self.no_bg, html_page=html_page, image=image)
        assert path.endswith('.png')
        image.save(path)
