PrivatBank (cards):
{% for curr in kurs %}
*{{ curr.ccy }}* : {{ curr.sale }}
{% endfor %}
