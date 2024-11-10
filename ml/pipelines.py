import torch
from tqdm import tqdm
from pprint import pprint
from typing import Literal

from opensearch import client, INDEX_NAME, save_doc
from transformer import model, process_doc


def process_collection():
    docs: list[list[dict[str, str]]] = [
        [
            {
                "description": """
  <1.pdf>
  1  РАЗВИТИЕ НОВЫХ КОММУНИКАЦИОННЫХ ИНТЕРНЕТ-ТЕХНОЛОГИЙ В РОССИИ И В МИРЕ В 2023 ГОДУ  С УЧАСТИЕМ
  2  ВВЕДЕНИЕ  1  Изучая внедрение новых технологий и активность пользователей, эксперты «Ростелекома» ежегодно проводят аналитические исследования в сфере развития коммуникационных сервисов. В периметр нового Проникновение социальных сетей в мире уже достигло 90%, при этом ожидается, что рост аудитории продолжится со средним темпом 4%. В 2023 году международные социальные сети начали использовать подписную модель  признана в РФ экстремистской организацией и запрещена в России кликабельная кнопка  исследования вошли основные события 2023 года на российском и глобальном рынке потребительских коммуникационных сервисов, которые определяют дальнейшие тенденции в ключевых направлениях. монетизации своих сервисов, предлагая пользователям получить официальный статус распространителя и создателя контента их платформы в обмен на ежемесячную плату. По оценкам The Economist, выручка от подписок может варьироваться от 1 до 3%  В 2023 году количество интернет-пользователей в мире продолжило увеличиваться. По итогам года 5,3 млрд человек или 65,7% мирового населения пользовались интернетом. Ежедневная аудитория Рунета достигла 95,3 млн человек, что составляет 66,4% от всего населения России, а количество доменов, зарегистрированных в зоне .RU, превысило 4,9 млн.  Современная цифровая инфра- структура позволяет сервисам и продуктам на базе новых коммуникационных интернет- технологий (НКИТ) постоянно развиваться и предоставлять пользователям уникальный опыт взаимодействия с контентом. За одну минуту в мировом интернете в 2023 году пользователи успевали:  2–3  Социальные сети и мессенджеры  E-MAIL  FACEBOOK *  TWITTER WHATSAPP *  INSTAGRAM  *  241 млн  4 млн 694 тыс.  360 тыс. 16,5 млн  ОТПРАВИТЬ ОТПРАВИТЬ ЛАЙКНУТЬ ОТПРАВИТЬ ОТПРАВИТЬ  ЭЛЕКТРОННЫХ ПИСЕМ  ПОСТОВ X-СООБЩЕНИЙ РОЛИКОВ ЧЕРЕЗ ЛИЧНЫЕ СООБЩЕНИЯ СООБЩЕНИЙ  принадлежит корпорации Meta, ◊  признанной экстремистской и запрещенной в России  Исследования прошлых лет  8 стр.
  потребители все реже выбирают только один видеосервис, предпочитая переключаться между платформами для доступа к их уникальному контенту. Уже около половины пользователей онлайн-кинотеатров в России предпочитает иметь подписки на от двух до четырех видеосервисов. По итогам 2023 года на первом месте по количеству платных подписчиков остался Кинопоиск, а на второе вышел онлайн-кинотеатр Wink. Видеоролики остаются крайне популярным форматом, практически все интернет-пользователи (92,3%) смотрят их на различных ресурсах. Несмотря на высокий уровень проникновения, крупнейший видеосервис YouTube продолжает наращивать аудиторию как по всему миру, так и в России. При этом в России отмечается приход российских пользователей Онлайн-кинотеатры в России заметно нарастили выручку и клиентскую базу. Они продолжают развивать собственное производство и активно защищают его от распространения на пиратских ресурсах. В итоге, с одной стороны, увеличивается средний чек на одного пользователя, что вызвано интересом зрителей к более дорогим расширенным подпискам. С другой стороны, растет и количество платных подписчиков из-за интереса к ориги- нальному контенту. При этом Игровой рынок продолжает восстанавливаться после падения на отечественные сервисы, что, однако, не привело к оттоку с зарубежных. Как и в случае с социальными сетями, на видеоплатформах появилось требование о маркировке авторами контента, отредактированного или созданного с помощью технологий искусственного интеллекта. 2022 года и отыгрывать снижение после пиков пандемийных лет.  Видеохостинги с пользовательским контентом  Онлайн-кинотеатры  Игровые сервисы  от выручки компании, доминирующей моделью монетизации по-прежнему является рекламная модель. Как в мире, так и в России наблюдается тенденция запрещать государственным служащим использовать зарубежные социальные сети и мессенджеры, а также переводить их на платформы коммуникационных сервисов национальной разработки. В России с 2023 года запрет на передачу персональных данных через зарубежные мессенджеры законодательно установлен для различных организаций, в т.ч. банков и финансовых организаций.  Введение  Проникновение AR/VR-сервисов в повседневную жизнь пользователей пока сдерживается отсутствием массового рынка гарнитур, ограниченным удобством устройств и популярного контента. Пик завышенных ожиданий от технологии VR/AR пройден, устройства доказали свою применимость, но в ограниченных кейсах применения. Исследователи пока не ожидают изменения динамики, однако прогнозируют активизацию роста, связанную с выходом решений новых поколений. Например, на рынке уже доступны решения в области разработки более точных и быстрых систем отслеживания, которые позволяют VR-изображениям следовать за движениями пользователя. Развитие цифровой инфраструктуры позволит устранить один из основных сдерживающих факторов массового распространения продуктов и сервисов в VR/AR.  Технологии виртуальной и дополненной реальности (B2C-сервисы)  Игровые студии ищут способы оптимизации бюджетов, используя новые технологии, чтобы ускорить и удешевить разработку. Например, внедряют более современные игровые движки и решения для автогенерации неигровых персонажей (NPC). В качестве одного из быстрорастущих трендов эксперты также выделяют кроссплатформенность, которая позволяет игрокам играть в игры на различных устройствах и платформах. Многие страны осознают, что компьютерные игры привлекают огромную пользовательскую аудиторию, поэтому еще несколько лет назад в мире наметился тренд на контроль за игровым контентом. В России государство также включается в создание контента с учетом национальных интересов.  4–5  34 стр.  26 стр.  20 стр.  44 стр.
  """
            }
        ]
    ]

    for doc in tqdm(docs):
        try:
            doc = process_doc(doc)
            save_doc(doc)
        except:
            print("Failed to process doc")


def find(query):
    with torch.no_grad():
        mean_pooled = model.encode(query)

    query = {
        "size": 2,
        "query": {"knn": {"embedding": {"vector": mean_pooled, "k": 2}}},
        "_source": False,
        "fields": ["id", "name", "description"],
    }

    response = client.search(body=query, index=INDEX_NAME)  # the same as before
    pprint(response["hits"]["hits"])
    return response["hits"]["hits"]