import calendar
import datetime

from django.db.models import Sum

from inoks.models import Profile, Order, earningPayments

# üyenin güncel ayının siparişi
from inoks.models.ProfileControlObjectNew import ProfileControlObjectNew


def monthlyMemberOrderTotal(profile):
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]

    orders_sum = Order.objects.filter(creationDate__range=(datetime_start, datetime_end)).filter(isApprove=True).filter(
        profile=profile).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


# üyenin seçilen ayının verdiği sipariş
def monthlyMemberOrderTotalByDate(profile, month, year):
    datetime_current = datetime.datetime.today()
    year = year
    month = month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]

    orders_sum = Order.objects.filter(creationDate__range=(datetime_start, datetime_end)).filter(isApprove=True).filter(
        profile=profile).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


# üyenin seçilen aya kadar vermiş olduğu sipariş tutarı
def MemberAllOrderTotalToDate(profile, month, year):
    year = year
    month = month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]

    orders_sum = Order.objects.filter(isApprove=True).filter(
        profile=profile).filter(creationDate__lte=datetime_end).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


# üyenin tüm zamanlarının sipariş tutarı(güncel aya kadar)
def MemberAllOrderTotal(profile):
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]

    orders_sum = Order.objects.filter(isApprove=True).filter(
        profile=profile).filter(creationDate__lte=datetime_end).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


# ağacı doldurur herkesin aylık ve toplam siparişlerini hesaplar
def returnLevelTreeNewVersion(profileArray, levelDict, level):
    profiles = []
    profiles = Profile.objects.filter(id__in=profileArray)
    profile_list = []

    for profile in profiles:
        total_order_month = monthlyMemberOrderTotal(profile)['total_price']
        if total_order_month is None:
            total_order_month = 0
            total_order_month = str(float(str(total_order_month).replace(",", ".")))

        total_order_all = MemberAllOrderTotal(profile)['total_price']
        if total_order_all is None:
            total_order_all = 0
            total_order_all = str(float(str(total_order_all).replace(",", ".")))

        profile_object = ProfileControlObjectNew(profile=profile, is_controlled=False,
                                                 total_order_month=total_order_month, total_order_all=total_order_all)
        profile_list.append(profile_object)

    levelDict[str(level)] = profile_list

    id_array = []

    if level < 7:
        for profile in profiles:

            profileSponsor = Profile.objects.filter(sponsor__id=profile.id)

            for sponsor in profileSponsor:
                id_array.append(sponsor.id)

        returnLevelTreeNewVersion(id_array, levelDict, level + 1)

    elif level == 7:
        return levelDict

    else:
        return 0


# ağacı doldurur herkesin aylık ve toplam siparişlerini hesaplar(girilen aya göre)
def returnLevelTreeNewVersionByDate(profileArray, levelDict, level, month, year):
    profiles = []
    profiles = Profile.objects.filter(id__in=profileArray)
    profile_list = []

    for profile in profiles:
        total_order_month = monthlyMemberOrderTotalByDate(profile, month, year)['total_price']
        if total_order_month is None:
            total_order_month = 0
            total_order_month = str(float(str(total_order_month).replace(",", ".")))

        total_order_all = MemberAllOrderTotalToDate(profile, month, year)['total_price']
        if total_order_all is None:
            total_order_all = 0
            total_order_all = str(float(str(total_order_all).replace(",", ".")))

        profile_object = ProfileControlObjectNew(profile=profile, is_controlled=False,
                                                 total_order_month=total_order_month, total_order_all=total_order_all)
        profile_list.append(profile_object)

    levelDict[str(level)] = profile_list

    id_array = []

    if level < 7:
        for profile in profiles:

            profileSponsor = Profile.objects.filter(sponsor__id=profile.id)

            for sponsor in profileSponsor:
                id_array.append(sponsor.id)

        returnLevelTreeNewVersionByDate(id_array, levelDict, level + 1, month, year)

    elif level == 7:
        return levelDict

    else:
        return 0


def calculate_order_of_tree(levelDict):
    order_totals = dict()
    order_month = 0
    order_all = 0

    for i in range(7):

        if i + 1 == 1:
            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

        if i + 1 == 2:

            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

        if i + 1 == 3:

            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

        if i + 1 == 4:

            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

        if i + 1 == 5:

            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

        if i + 1 == 6:

            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

        if i + 1 == 7:

            for orderPrice in levelDict[str(i + 1)]:
                order_month = order_month + float(orderPrice.total_order_month)
                order_all = order_all + float(orderPrice.total_order_all)

    order_totals['monthly_order'] = order_month
    order_totals['all_order'] = order_all
    return order_totals


def calculate_earning_of_tree(levelDict, total_order_member, month, year, past):
    earning = 0

    kademe = 0

    order_totals = calculate_order_of_tree(levelDict)

    total_order_all = order_totals['all_order']
    monthly_order = order_totals['monthly_order']

    total_order_member = total_order_member['total_price']

    if total_order_member is None:
        total_order_member = 0

    total_order1 = (monthly_order * 100) / 118

    if total_order_all >= 10648000:
        earning = float(total_order1 * 1 / 100)
        kademe = 10

    elif 4840000 <= total_order_all < 10648000:
        earning = float(total_order1 * 2 / 100)
        kademe = 9

    elif 2200000 <= total_order_all < 4840000:
        earning = float(total_order1 * 3 / 100)
        kademe = 8

    elif 1000000 <= total_order_all < 2200000:
        earning = float(total_order1 * 4 / 100)
        kademe = 7

    elif 607500 <= total_order_all < 1000000:
        earning = float(total_order1 * 1 / 100)
        kademe = 6

    elif 202500 <= total_order_all < 607500:
        earning = float(total_order1 * 2 / 100)
        kademe = 5

    elif 67500 <= total_order_all < 202500:
        earning = float(total_order1 * 3 / 100)
        kademe = 4

    elif 22500 <= total_order_all < 67500:
        earning = float(total_order1 * 4 / 100)
        kademe = 3

    elif 7500 <= total_order_all < 22500:
        if len(levelDict[str(3)]) == 9:





            earning = float(total_order1 * 5 / 100)
            kademe = 2
        elif len(levelDict[str(2)]) == 3:

            if earningPayments.objects.filter(profile=levelDict[str(1)][0].profile).count() == 0:
                if past:
                    tree_info_array = percent6ruleByDate(levelDict[str(1)][0].profile, month, year)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree']['percent'] == 6:
                            total_order_all = total_order_all - tree_info['tree_all_order']
                        # dictler döndürelecek ve sipariş miktarı düşürülecek

                else:
                    tree_info_array = percent6rule(levelDict[str(1)][0].profile)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree']['percent'] == 6:
                            total_order_all = total_order_all - tree_info['tree_all_order']
                        # dictler döndürelecek ve sipariş miktarı düşürülecek
                earning = total_order_all * 100 / 118
                earning = float(earning * 6 / 100)
            else:
                # total_order1 = (monthly_order * 100) / 118
                if past:
                    tree_info_array = percent6ruleByDate(levelDict[str(1)][0].profile, month, year)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree']['percent'] == 6:
                            total_order1 = total_order1 - (tree_info['tree_monthly_order'] * 100 / 118)
                        # dictler döndürelecek ve sipariş miktarı düşürülecek

                else:
                    tree_info_array = percent6rule(levelDict[str(1)][0].profile)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree']['percent'] == 6:
                            total_order1 = total_order1 - (tree_info['tree_monthly_order'] * 100 / 118)
                        # dictler döndürelecek ve sipariş miktarı düşürülecek

                earning = float(total_order1 * 6 / 100)



            #earning = float(total_order1 * 6 / 100)
            kademe = 1
        else:
            earning = 0

    elif 2500 <= total_order_all < 22500:
        if len(levelDict[str(2)]) >= 3:
            if earningPayments.objects.filter(profile=levelDict[str(1)][0].profile).count() == 0:
                if past:
                    tree_info_array = percent6ruleByDate(levelDict[str(1)][0].profile, month, year)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree'] == 6:
                            total_order_all = total_order_all - tree_info['tree_all_order']
                        # dictler döndürelecek ve sipariş miktarı düşürülecek

                else:
                    tree_info_array = percent6rule(levelDict[str(1)][0].profile)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree'] == 6:
                            total_order_all = total_order_all - tree_info['tree_all_order']
                        # dictler döndürelecek ve sipariş miktarı düşürülecek
                earning = total_order_all * 100 / 118
                earning = float(earning * 6 / 100)
            else:
                #total_order1 = (monthly_order * 100) / 118
                if past:
                    tree_info_array = percent6ruleByDate(levelDict[str(1)][0].profile, month, year)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree'] == 6:
                            total_order1 = total_order1 - (tree_info['tree_monthly_order']*100/118)
                        # dictler döndürelecek ve sipariş miktarı düşürülecek

                else:
                    tree_info_array = percent6rule(levelDict[str(1)][0].profile)
                    for tree_info in tree_info_array:

                        if tree_info['percent_tree'] == 6:
                            total_order1 = total_order1 - (tree_info['tree_monthly_order'] * 100 / 118)
                        # dictler döndürelecek ve sipariş miktarı düşürülecek

                earning = float(total_order1 * 6 / 100)
            kademe = 1
        else:
            earning = 0

    else:
        earning = 0

        kademe = 0
        # earning = 0

    # kademeye göre sipariş kontrolü
    if kademe == 0:
        earning = 0

    elif kademe == 1:
        if total_order_member >= 60:
            earning = earning
        else:
            earning = 0

    elif kademe == 2:
        if total_order_member >= 60:
            earning = earning
        else:
            earning = 0

    elif kademe == 3:
        if total_order_member >= 60:
            earning = earning
        else:
            earning = 0

    elif kademe == 4:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 5:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 6:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 7:
        if total_order_member >= 240:
            earning = earning
        else:
            earning = 0

    elif kademe == 8:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 9:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 10:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    else:
        earning = 0

    return earning


def return_level_of_profile(total_order_all, levelDict):
    kademe = ''
    if total_order_all >= 10648000:

        kademe = 10

    elif 4840000 <= total_order_all < 10648000:

        kademe = 9

    elif 2200000 <= total_order_all < 4840000:

        kademe = 8

    elif 1000000 <= total_order_all < 2200000:

        kademe = 7

    elif 607500 <= total_order_all < 1000000:

        kademe = 6

    elif 202500 <= total_order_all < 607500:

        kademe = 5

    elif 67500 <= total_order_all < 202500:

        kademe = 4

    elif 22500 <= total_order_all < 67500:

        kademe = 3

    elif 7500 <= total_order_all < 22500:
        if len(levelDict[str(3)]) == 9:

            kademe = 2
        elif len(levelDict[str(2)]) == 3:

            kademe = 1
        else:
            earning = 0

    elif 2500 <= total_order_all < 22500:
        if len(levelDict[str(2)]) == 3:
            kademe = 1

    return kademe


def calculate_percent_of_tree(levelDict, total_order_member, past, date):
    earning = 0

    kademe = 0
    percent = 0

    order_totals = calculate_order_of_tree(levelDict)

    total_order_all = order_totals['all_order']
    monthly_order = order_totals['monthly_order']

    total_order_member = total_order_member['total_price']

    if total_order_member is None:
        total_order_member = 0

    total_order1 = (monthly_order * 100) / 118

    if total_order_all >= 10648000:
        earning = float(total_order1 * 1 / 100)
        kademe = 10
        percent = 1

    elif 4840000 <= total_order_all < 10648000:
        earning = float(total_order1 * 2 / 100)
        kademe = 9
        percent = 2

    elif 2200000 <= total_order_all < 4840000:
        earning = float(total_order1 * 3 / 100)
        kademe = 8
        percent = 3

    elif 1000000 <= total_order_all < 2200000:
        earning = float(total_order1 * 4 / 100)
        kademe = 4
        percent = 4

    elif 607500 <= total_order_all < 1000000:
        earning = float(total_order1 * 1 / 100)
        kademe = 6
        percent = 1

    elif 202500 <= total_order_all < 607500:
        earning = float(total_order1 * 2 / 100)
        kademe = 5
        percent = 2

    elif 67500 <= total_order_all < 202500:
        earning = float(total_order1 * 3 / 100)
        kademe = 4
        percent = 3

    elif 22500 <= total_order_all < 67500:
        earning = float(total_order1 * 4 / 100)
        kademe = 3
        percent = 4

    elif 7500 <= total_order_all < 22500:
        if len(levelDict[str(3)]) == 9:
            earning = float(total_order1 * 5 / 100)
            kademe = 2
            percent = 5
        elif len(levelDict[str(2)]) == 3:
            earning = float(total_order1 * 6 / 100)
            kademe = 1
            percent = 6
        else:
            earning = 0

    elif 2500 <= total_order_all < 22500:
        if len(levelDict[str(2)]) == 3:
            if earningPayments.objects.filter(profile=levelDict[str(1)][0].profile).count() == 0:

                earning = total_order_all * 100 / 118
                earning = float(earning * 6 / 100)
                percent = 6
            else:
                earning = float(total_order1 * 6 / 100)
                percent = 6
            kademe = 1
        else:
            earning = 0

    else:
        earning = 0

        kademe = 0
        # earning = 0

    # kademeye göre sipariş kontrolü
    if kademe == 0:
        earning = 0
        percent = 0

    elif kademe == 1:
        if total_order_member >= 60:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 2:
        if total_order_member >= 60:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 3:
        if total_order_member >= 60:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 4:
        if total_order_member >= 120:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 5:
        if total_order_member >= 120:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 6:
        if total_order_member >= 120:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 7:
        if total_order_member >= 240:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 8:
        if total_order_member >= 120:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 9:
        if total_order_member >= 120:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    elif kademe == 10:
        if total_order_member >= 120:
            earning = earning
            percent = percent
        else:
            earning = 0
            percent = 0

    else:
        earning = 0
        percent = 0

    tree_feature = dict()
    tree_feature['percent'] = percent
    tree_feature['earning'] = earning
    return tree_feature


def percent6rule(profile):
    profiles = Profile.objects.filter(sponsor=profile)
    levelDict1 = dict()
    levelDict2 = dict()
    levelDict3 = dict()
    profile_array1 = []
    profile_array2 = []
    profile_array3 = []

    tree_info_array = []

    for profile in profiles:
        profile_array1 = []
        profile_array1.append(profile.id)
        levelDict1 = dict()
        treeInfoDict = dict()
        returnLevelTreeNewVersion(profile_array1, levelDict1, 1)
        order_total_member1 = monthlyMemberOrderTotal(profile, )
        percent = calculate_percent_of_tree(levelDict1, order_total_member1, False, None)
        x = calculate_order_of_tree(levelDict1)
        tree_order = x['monthly_order']
        tree_all_order = x['all_order']
        treeInfoDict['percent_tree'] = percent
        treeInfoDict['tree_monthly_order'] = tree_order
        treeInfoDict['tree_all_order'] = tree_all_order
        tree_info_array.append(treeInfoDict)

    """profile_array2.append(profile[1])
    returnLevelTreeNewVersion(profile_array2, levelDict2, 1)
    order_total_member2 = monthlyMemberOrderTotal(profile[1], )
    total_earning2 = calculate_percent_of_tree(levelDict2, order_total_member2, False, None)
    tree_price2 = calculate_order_of_tree(levelDict2)['monthly_order']

    profile_array3.append(profile[2])
    returnLevelTreeNewVersion(profile_array3, levelDict3, 1)
    order_total_member3 = monthlyMemberOrderTotal(profile[2], )
    total_earning3 = calculate_percent_of_tree(levelDict3, order_total_member3, False, None)
    tree_price3 = calculate_order_of_tree(levelDict3)['monthly_order']"""

    return tree_info_array


def percent6ruleByDate(profile, month, year):
    profiles = Profile.objects.filter(sponsor=profile)
    levelDict1 = dict()
    levelDict2 = dict()
    levelDict3 = dict()
    profile_array1 = []
    profile_array2 = []
    profile_array3 = []

    tree_info_array = []

    for profile in profiles:
        profile_array1 = []
        profile_array1.append(profile.id)
        levelDict1 = dict()
        treeInfoDict = dict()
        returnLevelTreeNewVersionByDate(profile_array1, levelDict1, 1, month, year)
        order_total_member1 = monthlyMemberOrderTotalByDate(profile, month, year)
        percent = calculate_percent_of_tree(levelDict1, order_total_member1, False, None)
        x = calculate_order_of_tree(levelDict1)
        tree_order = x['monthly_order']
        tree_all_order = x['all_order']
        treeInfoDict['percent_tree'] = percent
        treeInfoDict['tree_monthly_order'] = tree_order
        treeInfoDict['tree_all_order'] = tree_all_order
        tree_info_array.append(treeInfoDict)

    """profile_array2.append(profile[1])
    returnLevelTreeNewVersion(profile_array2, levelDict2, 1)
    order_total_member2 = monthlyMemberOrderTotal(profile[1], )
    total_earning2 = calculate_percent_of_tree(levelDict2, order_total_member2, False, None)
    tree_price2 = calculate_order_of_tree(levelDict2)['monthly_order']

    profile_array3.append(profile[2])
    returnLevelTreeNewVersion(profile_array3, levelDict3, 1)
    order_total_member3 = monthlyMemberOrderTotal(profile[2], )
    total_earning3 = calculate_percent_of_tree(levelDict3, order_total_member3, False, None)
    tree_price3 = calculate_order_of_tree(levelDict3)['monthly_order']"""

    return tree_info_array
