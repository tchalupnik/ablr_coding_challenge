from rest_framework import serializers


class AccountBalanceSerializer(serializers.Serializer):
    ordinary_account = serializers.DecimalField(
        source="oa.value", max_digits=20, decimal_places=2
    )
    special_account = serializers.DecimalField(
        source="sa.value", max_digits=20, decimal_places=2
    )
    medisave_account = serializers.DecimalField(
        source="ma.value", max_digits=20, decimal_places=2
    )


class ContributionSerializer(serializers.Serializer):
    for_month = serializers.CharField(source="month.value")
    paid_on = serializers.CharField(source="date.value")
    amount = serializers.DecimalField(
        source="amount.value", max_digits=20, decimal_places=2
    )
    employer = serializers.CharField(source="employer.value")


class AssessmentSerializer(serializers.Serializer):
    year = serializers.DateField(format="Y", source="yearofassessment.value")
    employment = serializers.DecimalField(
        source="employment.value", max_digits=20, decimal_places=2
    )
    trade = serializers.DecimalField(
        source="trade.value", max_digits=20, decimal_places=2
    )
    interest = serializers.DecimalField(
        source="interest.value", max_digits=20, decimal_places=2
    )
    rent = serializers.DecimalField(
        source="rent.value", max_digits=20, decimal_places=2
    )
    total = serializers.DecimalField(
        source="amount.value", max_digits=20, decimal_places=2
    )
    tax_clearance = serializers.CharField(source="taxclearance.value")


class AddressSerializer(serializers.Serializer):
    block = serializers.CharField(source="block.value")
    street = serializers.CharField(source="street.value")
    building = serializers.CharField(source="building.value")
    floor = serializers.CharField(source="floor.value")
    postal = serializers.CharField(source="postal.value")


class PersonSerializer(serializers.Serializer):
    id = serializers.CharField(source="uinfin.value")
    name = serializers.CharField(source="name.value")
    email = serializers.EmailField(source="email.value")
    mobile = serializers.SerializerMethodField()
    address = AddressSerializer(source="regadd")
    housing_type = serializers.CharField(source="hdbtype.desc")
    sex = serializers.CharField(source="sex.desc")
    race = serializers.CharField(source="race.desc")
    nationality = serializers.CharField(source="nationality.desc")
    birth_at = serializers.DateField(source="dob.value", format="yyyy-MM-dd")
    birth_in = serializers.CharField(source="birthcountry.desc")
    residential_status = serializers.CharField(source="residentialstatus.desc")
    account_balance = AccountBalanceSerializer(source="cpfbalances")
    assessment_history = AssessmentSerializer(many=True, source="noahistory.noas")
    contribution_history = ContributionSerializer(
        many=True, source="cpfcontributions.history"
    )

    def get_mobile(self, obj):
        return (
            obj["mobileno"]["prefix"]["value"]
            + obj["mobileno"]["areacode"]["value"]
            + obj["mobileno"]["nbr"]["value"]
        )


class AuthoriseUrlSerializer(serializers.Serializer):
    url = serializers.URLField()


class ReceiveTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
