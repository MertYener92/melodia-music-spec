"""
Musik jeton havuzu -- SADECE muzik (sarki + music-spec) icin. melodia-backend
generate.js'teki creditPlans.js ile BIREBIR AYNI degerleri kullanir --
ikisi de UsersTable.aiCreditsUsed/aiCreditsPeriod/plan alanlarini okuyup
yazdigi icin, buradaki degerler orada tanimlananla senkron KALMAK ZORUNDA.
Biri degisirse digeri de degismeli.

UC PLAN, IKI FARKLI SIFIRLAMA DONGUSU:
 - pro_weekly:  25 jeton, HAFTALIK sifirlanir
 - pro_monthly: 120 jeton, AYLIK sifirlanir
 - pro_yearly:  120 jeton, AYLIK sifirlanir (yillik odeme sadece
   FATURALAMA sikligini degistiriyor, jeton mantigi pro_monthly ile
   birebir ayni)
"""

from datetime import datetime, timezone, timedelta

AI_CREDIT_LIMITS = {
    "free": 10**9,
    "pro_weekly": 25,
    "pro_monthly": 120,
    "pro_yearly": 120,
}


def limit_for_plan(plan: str) -> int:
    return AI_CREDIT_LIMITS.get(plan, AI_CREDIT_LIMITS["free"])


def _iso_week_key(now: datetime) -> str:
    # ISO hafta numarasi (Pazartesi-Pazar), orn. "2026-W37". generate.js'teki
    # isoWeekKey ile ayni sonucu vermesi icin Python'un kendi ISO takvim
    # hesaplamasi (isocalendar) kullaniliyor.
    iso_year, iso_week, _ = now.isocalendar()
    return f"{iso_year}-W{iso_week}"


def current_period_key(plan: str, now: datetime = None) -> str:
    if now is None:
        now = datetime.now(timezone.utc)
    if plan == "pro_weekly":
        return _iso_week_key(now)
    return f"{now.year}-{now.month}"