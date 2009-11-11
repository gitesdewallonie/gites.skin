from dateutil.relativedelta import relativedelta
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName
from gites.skin import GitesMessage as _
from gites.skin import GitesLocalesMessage as localTranslate

from gites.core.content.ideesejour import IdeeSejour
from interfaces import (ISearchHebergement,
                        IBasicSearchHebergement,
                        IBasicSearchHebergementTooMuch,
                        ISearchHebergementTooMuch)
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.sqlalchemy import getSAWrapper
from sqlalchemy import and_, or_, select
import plone.z3cform.z2


class SearchHebergement(formbase.PageForm):
    """
    A search module to search hebergement
    """
    label = _("Search Hebergement")
    form_reset = False

    form_fields = form.FormFields(ISearchHebergement)
    too_much_form_fields = form.FormFields(ISearchHebergementTooMuch)

    search_results = ViewPageTemplateFile('templates/search_results_hebergement.pt')

    def update(self):
        self.request.locale = plone.z3cform.z2.setup_locale(self.request)
        super(SearchHebergement, self).update()

    def translateGroupedType(self, groupedType):
        """
        Translate a grouped type to a list of types
        """
        if groupedType == -2:
            types = ['GR', 'GF', 'MT', 'GC', 'MV', 'GRECR', 'GG']
        elif groupedType == -3:
            types = ['CH', 'MH', 'CHECR']
        return self.translateTypes(types)

    def translateTypes(self, types):
        """
        Translate types to a list of types
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        typeHebTable = wrapper.getMapper('type_heb')
        typeList = session.query(typeHebTable).filter(typeHebTable.type_heb_code.in_(types))
        return [typeHeb.type_heb_pk for typeHeb in typeList]

    @form.action(localTranslate(u"Search"))
    def action_search(self, action, data):
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        hebergementTable = wrapper.getMapper('hebergement')
        proprioTable = wrapper.getMapper('proprio')
        reservationsTable = wrapper.getMapper('reservation_proprio')
        provincesTable = wrapper.getMapper('province')
        episTable = wrapper.getMapper('link_hebergement_epis')
        hebergementType = data.get('hebergementType')
        provinces = data.get('provinces')
        classification = data.get('classification')
        capacityMin = data.get('capacityMin')
        roomAmount = data.get('roomAmount')
        checkAnimals = data.get('animals')
        checkSmokers = data.get('smokers')
        fromDate = data.get('fromDate')
        toDate = data.get('toDate')
        seeResults = self.request.form.has_key('form.seeResults')

        query = session.query(hebergementTable).join('province').join('proprio').outerjoin('reservations')
        query = query.filter(hebergementTable.heb_site_public == '1')
        query = query.filter(proprioTable.pro_etat == True)

        if provinces and provinces != -1:
            query = query.filter(provincesTable.prov_pk == provinces)
        if hebergementType and hebergementType != -1:
            if hebergementType in [-2, -3]:
                groupedHebergementTypes = self.translateGroupedType(hebergementType)
                query = query.filter(hebergementTable.heb_typeheb_fk.in_(groupedHebergementTypes))
            else:
                query = query.filter(hebergementTable.heb_typeheb_fk == hebergementType)
        if classification and classification != -1:
            query = query.filter(and_(episTable.heb_nombre_epis == classification,
                                      hebergementTable.heb_pk==episTable.heb_pk))
        if checkAnimals:
            query = query.filter(hebergementTable.heb_animal=='oui')
        if checkSmokers:
            query = query.filter(hebergementTable.heb_fumeur=='oui')
        if roomAmount:
            query = query.filter(hebergementTable.heb_cgt_nbre_chmbre >= roomAmount)
        if capacityMin:
            if capacityMin < 16:
                capacityMax = capacityMin + 4
                query = query.filter(or_(hebergementTable.heb_cgt_cap_min.between(capacityMin, capacityMax),
                                         hebergementTable.heb_cgt_cap_max.between(capacityMin, capacityMax)))
            else:
                capacityMax = capacityMin
                capacityMin = 16
                query = query.filter(and_(hebergementTable.heb_cgt_cap_min >= capacityMin,
                                          hebergementTable.heb_cgt_cap_max >= capacityMax))

        if fromDate or toDate:
            query = query.filter(hebergementTable.heb_calendrier_proprio != 'non actif')
            # on ne considère que les hébergements pour lequel le calendrier
            # est utilisé
            beginDate = fromDate or (toDate + relativedelta(days=-1))
            endDate = toDate or (fromDate + relativedelta(days=+1))
            # il ne peut pas y avoir d'enregistrement dans la table de
            # réservations entre les dates de début et de fin (vu que seules
            # les indisponibilités sont dans la table)

            # il y a un décalage dans le calcul des jours / nuits :
            # 1 nuit indiquée comme louée = 2 jours demandés
            # --> >= beginDate et < endDate
            busyHebQuery = session.query(reservationsTable)
            busyHeb = select([reservationsTable.heb_fk],
                             and_(reservationsTable.res_date >= beginDate,
                                  reservationsTable.res_date < endDate)).distinct().execute().fetchall()
            busyHebPks = [heb.heb_fk for heb in busyHeb]
            query = query.filter(~hebergementTable.heb_pk.in_(busyHebPks))

        if isinstance(self.context, IdeeSejour):
            sejour = self.context
            filteredHebergements = sejour.getHebergements()
            query = query.filter(hebergementTable.heb_pk.in_(filteredHebergements))

        query = query.order_by(hebergementTable.heb_nom)
        self.selectedHebergements = [hebergement.__of__(self.context.hebergement) for hebergement in query.all()]

        nbResults = len(self.selectedHebergements)
        translation_service = getToolByName(self.context,
                                            'translation_service')

        utranslate = translation_service.utranslate
        lang = self.request.get('LANGUAGE', 'en')
        if nbResults > 50 and not seeResults:   #il faut affiner la recherche
            self.form_fields = self.too_much_form_fields
            form.FormBase.resetForm(self)
            self.widgets['roomAmount'].setRenderedValue(roomAmount)
            self.widgets['capacityMin'].setRenderedValue(capacityMin)
            self.widgets['animals'].setRenderedValue(checkAnimals)
            self.widgets['smokers'].setRenderedValue(checkSmokers)
            self.widgets['hebergementType'].setRenderedValue(hebergementType)
            self.widgets['provinces'].setRenderedValue(provinces)
            self.widgets['classification'].setRenderedValue(classification)
            self.widgets['fromDate'].setRenderedValue(fromDate)
            self.widgets['toDate'].setRenderedValue(toDate)

            message = utranslate('gites',
                                 "La recherche a renvoy&eacute; ${nbr} r&eacute;sultats. <br /> Il serait utile de l'affiner.",
                                 {'nbr': nbResults},
                                 target_language=lang,
                                 context=self.context)
            self.errors += (message,)
            self.status = " "
            return self.template()

        else:   #on montre tous les resultats, independamment du nombre
            if nbResults == 0:
                message = utranslate('gites',
                                     "La recherche n'a pas renvoy&eacute; de r&eacute;sultats.",
                                     target_language=lang,
                                     context=self.context)
                self.errors += (message,)
                self.status = " "
                return self.template()
            else:
                return self.search_results()


class BasicSearchHebergement(SearchHebergement):
    """
    A search module to search hebergement
    """
    label = _("Search Hebergement")
    form_reset = False

    form_fields = form.FormFields(IBasicSearchHebergement)
    too_much_form_fields = form.FormFields(IBasicSearchHebergementTooMuch)

    search_results = ViewPageTemplateFile('templates/search_results_hebergement.pt')

    def update(self):
        self.request.locale = plone.z3cform.z2.setup_locale(self.request)
        super(BasicSearchHebergement, self).update()
