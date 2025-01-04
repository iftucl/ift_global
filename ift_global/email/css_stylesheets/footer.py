import datetime

footer = """
<footer class="email-footer">
    <div class="footer-bottom">
        <h3>Quick Links</h3>
        <table class="footer-table">
            <tr>
                <th><a href="#placeholder">UCL - Institute for Finance & Technology</a></th>
                <th><a href="#placeholder">About Us</a></th>
                <th><a href="#placeholder">Services</a></th>
                <th><a href="mailto: ift@ucl.ac.uk">Contact</a></th>
            </tr>
        </table>
        <br>
        <p>&copy; {} UCL - IFT. All rights reserved.</p>
    </div>
</footer>
""".format(datetime.datetime.now().year)
