from Products.Five import BrowserView
from zope.interface import implements
from zope.security.interfaces import Unauthorized
from interfaces import ILogoView


class LogoView(BrowserView):
    """
    Logo
    """
    implements(ILogoView)

    def safe_getattr(self, obj, attr, default):
        """Attempts to read the attr, returning default if Unauthorized."""
        try:
            return getattr(obj, attr, default)
        except Unauthorized:
            return default

    def getLogoUrl(self):
        """
        return the default url of the logo
        """
        banner = self.safe_getattr(self.context, 'banner.jpg', None)
        if banner:
            banner_translation = banner.getTranslation()
            if banner_translation:
                banner = banner_translation
            return banner.tag()
        logo = getattr(self.context, 'logo.jpg')
        return logo.tag()

    def getButton(self, image):
        """
        Return correct button regarding language
        """
	try:
            image = self.safe_getattr(self.context, image, None)
            if image:
                image_translation = image.getTranslation()
                if image_translation:
                    image = image_translation
                return image.tag()
        except:
	    return ''
