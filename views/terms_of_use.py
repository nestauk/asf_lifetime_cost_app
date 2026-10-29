"""Terms of use page."""

import streamlit as st

from components.layout import render_page_title

# Center content
left_pad, main_col, right_pad = st.columns([1, 12, 1])

with main_col:
    render_page_title(
        title="Terms of use",
    )
    st.markdown(
        """
        <div style="font-size:15px; color:#333; line-height:1.7; margin-bottom:10px;">
        This website is owned and operated by <a href="https://www.nesta.org.uk" target="_blank" style="color: #0000FF; text-decoration: underline;">Nesta</a> - 
        you can find our full details below. Use of the site is subject to these Terms.
        Our Privacy Notice explains how we use personal information which we may collect via the site. If you don’t agree with these
        Terms or our Privacy Notice, please don’t use this site.<br><br>

        This website is intended to be used by policy analysts, researchers, government, and sector specialists for non-commercial research and analysis only.<br><br>

        1. The information, materials and logos on this site (including any downloadable materials) belong to Nesta, our partners or licensors. Unless otherwise indicated,
        materials and resources owned by Nesta are licensed for use under a
        <a href="https://www.nesta.org.uk" target="_blank" style="color: #0000FF; text-decoration: underline;">Creative Commons Attribution NonCommercial ShareAlike licence (CC-BY-NC-SA)</a>.
        We make no representation or warranty about the content, including in relation to non-infringement of intellectual property rights.

        2. Nesta cannot compensate you for any loss you may suffer as a result of:
            * action you take based on anything you read on these pages;
            * any mistake with the content on our website;
            * any parts of our website being unavailable or inaccessible;
            * your use of any organisation’s website that you can access from our website
                (including any purchase from that organisation and any use they make of the personal data you provide to them);
                the downloading of any material from any of our website.<br><br>
            
        3. Nesta will not exclude any liability we may have in the unlikely event we have been fraudulent or if we are negligent and as a result we cause death or personal injury in connection with this website.

        4. All content from the site may be printed, copied or downloaded provided that it is for private and personal use. You must not use any content for commercial gain. In the event that you do print, copy or
        download the content, you must always cite Nesta as the content creator. You will be responsible for any damage to your computer system that may result from the downloading of any content or any other harm
        (save as provided for otherwise elsewhere here) that arises as a result of your use of the content.

        5. When you download or export data files (e.g., Excel spreadsheets or charts) you must keep intact all embedded licensing notices, copyright tags, and source attributions provided within the file.

        6. You must not use automated scripts, bots, crawlers or web-scraping tools to query the application, extract underlying datasets, or flood the application with automated requests, including but not
        limited to in any manner that may degrade service performance for other users.

        7. You must not use this site:
            * to post, share or transmit material which is unlawful or infringes anyone else’s rights
            * for any commercial purpose
            * in any way which is abusive, defamatory or obscene or which harasses or distresses anyone or restricts or inhibits their use and enjoyment of the site or otherwise damages our reputation
            * to transmit software viruses or code designed to interrupt, destroy or compromise the integrity of computer software, hardware or telecommunications equipment.<br><br>
        
        8. You are responsible for any comments, text, video, audio, images or other content which you post on the site and must obtain any relevant permissions or
        consents to post this content. You grant us a perpetual, worldwide,non-exclusive, royalty-free and fully transferable right to copy, download, distribute, transmit
        and adapt your content and waive your moral rights in it.

        9. We are not responsible for content posted on the site by users and third parties. The views expressed are not necessarily the views of Nesta or our partners.
        You can report any inappropriate content to us at <a href="mailto:information@nesta.org.uk" style="color: #0000FF; text-decoration: underline;">information@nesta.org.uk</a>.
        Although we don’t monitor all content posted on the site, we reserve the right to do so and to edit or remove content at our absolute discretion and without notice.

        10. When using this site, you must comply with the following conditions:
            * act lawfully, ethically and in good faith and comply with these Terms;
            * acknowledge that the results generated by the tool depend directly on the inputs and parameters you select in the sidebar. You are solely responsible for verifying the accuracy and appropriateness of any custom parameters you enter;
                understand that default parameters loaded in the sidebar represent generic illustrative benchmarks and do not guarantee accuracy for any specific building, geographical location or commercial scenario;
            * treat all calculated outputs, cost comparisons and financial figures as illustrative, indicative estimates for exploratory purposes only;
            * if you share or distribute results, charts or exported files from this tool, you must accurately attribute the tool and clearly state the input assumptions used to generate those figures;
            * act with common sense, integrity and treat others with respect;
            * do not lie, misrepresent something or someone, or pretend to be someone else;
            * be polite and respectful when you communicate or interact with others.<br><br>
        
        11. As permitted by law, you shall release, defend (at Nesta’s option), indemnify, and hold Nesta harmless from and against any claims, liabilities, damages, losses, and expenses, including, without limitation, all reasonable
        legal and professional fees, arising from or in any way connected with: (a) your breach of these Terms, (b) your improper use of the platform. This indemnity shall only apply if and to the extent that the claims, liabilities,
        damages, losses, and expenses have been caused by your breach of obligations under these Terms.

        12. The content and information on this site is provided for general information only. It is not intended to amount to advice that you should rely on. You should obtain your own professional or specialist advice before taking
        any action or inaction on the basis of content on this site. For the avoidance of doubt, calculations and cost comparisons generated by the tool rely on simplified baseline economic models and parameters (such as energy price
        forecasts, SCOP/efficiency ratings, and installation cost estimates). These models are illustrative abstractions. Outputs must not be used as the basis for consumer purchasing decisions or formal contractual commitments.

        13. The content and information on this site is subject to change from time to time and we make no representations, warranties or guarantees, whether expressed or implied, that the content on our site is accurate, complete
        or up-to-date. We are not responsible for the content of external sites which you link to from this site.

        14. We don’t guarantee that the site will always be available or free from errors or viruses. You are responsible for installing virus-checking software to protect your hardware. As far as legally possible, we and our
        partners exclude all liability for any loss or damage suffered as a result of using or accessing our site, whether direct or indirect, and however arising, including any loss of data or damage caused by downloading content from our site.

        15. This tool is hosted on cloud infrastructure. We do not guarantee uninterrupted uptime, server performance, or compatibility across all web browsers or devices.

        16. These Terms may be varied from time to time. If you use the site after any change has been made, you will be deemed to have accepted the change.
        Additional terms may apply to certain areas of this site, such as applications for grant funding or payment for events.

        17. These Terms are governed by English law and the courts of England and Wales will have jurisdiction over any dispute arising from them.

        Nesta, a company limited by guarantee registered in England and Wales with company number 7706036 and charity number 1144091. Registered as a charity in Scotland number SC042833.<p>

        Registered office: 58 Victoria Embankment, London EC4Y 0DS.
        </div>
        """,
        unsafe_allow_html=True,
    )
