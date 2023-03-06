from markdown2anki.md_2_anki.process_images import get_images_sources


class TestGetImagesSources:
    def test_good_case(self):
        images_input = (
            '<img src="something.png">'
            '<img class="a-class" src="ALSKDJJSNDaksj">'
            '<img src="something.png">'
        )
        expected_output = {"ALSKDJJSNDaksj", "something.png"}
        images_sources = get_images_sources(images_input)
        assert images_sources == expected_output

    def test_hyperlink_case(self):
        images_input = (
            '<img src="https://i.redd.it/754vnky90lfa1.jpg">'
            '<img src="something.png">'
        )
        expected_output = {"something.png"}
        images_sources = get_images_sources(images_input)
        assert images_sources == expected_output

    def test_uppercase_edge_case(self):
        images_input = (
            '<IMG SRC="HTTPS://I.REDD.IT/754VNKY90LFA1.JPG">'
            '<IMG SRC="SOMETHING.PNG">'
        )
        expected_output = {"SOMETHING.PNG"}
        images_sources = get_images_sources(images_input)
        assert images_sources == expected_output
