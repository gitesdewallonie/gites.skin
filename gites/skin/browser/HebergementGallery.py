from Products.Five import BrowserView
from zope.interface import implements
from gites.skin.browser.interfaces import IHebergementGallery

class HebergementGallery(BrowserView):
   """
   View for the gallery of an hebergement
   """
   implements(IHebergementGallery)

   def getVignettesUrl(self):
       """
        Get the vignette of an hebergement
       """
       vignettes=[]
       codeGDW = self.context.heb_code_gdw
       listeImage = self.context.photos_heb.fileIds()
       for i in range(15):
            if i < 10:
                photo="%s0%s.jpg"%(codeGDW,i)
            else:
                photo="%s%s.jpg"%(codeGDW, i)
            if photo in listeImage:
                vignettes.append(photo)
       return vignettes

