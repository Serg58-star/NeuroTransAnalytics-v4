"""
Метаданные тестов СЗР - полные параметры псевдо-случайных последовательностей
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import sqlite3
import logging

logger = logging.getLogger(__name__)

# Базовые константы (существующие)
SYSTEM_PARAMETERS = {
    "MaxRedLight": 2000,
    "MinRedLight": 135,
    "ROTATE_PERIOD": 400,
    "POKAZ_COUNT": 36,
    "NoUchtPOKAZ_COUNT": 3
}

STIMULUS_POSITIONS = {
    "left": "слева",
    "center": "центр",
    "right": "справа"
}

STIMULUS_COLORS = {
    "red": "красный",
    "green": "зеленый",
    "blue": "синий"
}

TEST_TYPES = {
    "simple": "Простая зрительная реакция (ПЗР)",
    "color_red": "Реакция на цвет (красный)",
    "shift": "Реакция на сдвиг"
}


# Новые классы для управления метаданными
@dataclass
class StimulusMetadata:
    """Метаданные одного стимула"""
    stimulus_number: int
    color: str
    position: str
    prestimulus_interval: int
    circle_sequence: Optional[str] = None
    shift_parameter: Optional[int] = None


@dataclass
class TestMetadata:
    """Метаданные полного теста (36 стимулов)"""
    test_type: str
    stimuli: List[StimulusMetadata]

    def get_stimulus(self, number: int) -> StimulusMetadata:
        return self.stimuli[number - 1]

    def get_by_color(self, color: str) -> List[StimulusMetadata]:
        return [s for s in self.stimuli if s.color == color]

    def get_by_position(self, position: str) -> List[StimulusMetadata]:
        return [s for s in self.stimuli if s.position == position]


class TestMetadataManager:
    """
    Менеджер метаданных тестирования
    Централизованное хранилище параметров псевдо-случайных последовательностей
    """

    def __init__(self):
        self._metadata_cache: Dict[str, TestMetadata] = {}
        self._system_parameters = SYSTEM_PARAMETERS.copy()
        self._initialize_metadata()

    def _initialize_metadata(self):
        """Инициализация всех метаданных тестов из предоставленных таблиц"""

        # 1. ПРОСТОЙ ТЕСТ (simple/Tst1)
        simple_stimuli = [
            StimulusMetadata(1, "blue", "right", 1045),
            StimulusMetadata(2, "green", "left", 1840),
            StimulusMetadata(3, "red", "right", 2300),
            StimulusMetadata(4, "red", "center", 1200),
            StimulusMetadata(5, "green", "right", 1500),
            StimulusMetadata(6, "blue", "center", 1000),
            StimulusMetadata(7, "green", "left", 1700),
            StimulusMetadata(8, "red", "left", 950),
            StimulusMetadata(9, "green", "center", 1100),
            StimulusMetadata(10, "blue", "right", 1800),
            StimulusMetadata(11, "blue", "left", 970),
            StimulusMetadata(12, "red", "center", 2100),
            StimulusMetadata(13, "green", "center", 1300),
            StimulusMetadata(14, "red", "left", 1000),
            StimulusMetadata(15, "green", "right", 1510),
            StimulusMetadata(16, "blue", "center", 2000),
            StimulusMetadata(17, "blue", "left", 1100),
            StimulusMetadata(18, "red", "left", 1255),
            StimulusMetadata(19, "green", "center", 920),
            StimulusMetadata(20, "blue", "right", 1900),
            StimulusMetadata(21, "red", "center", 970),
            StimulusMetadata(22, "green", "right", 1165),
            StimulusMetadata(23, "blue", "left", 1850),
            StimulusMetadata(24, "red", "right", 1430),
            StimulusMetadata(25, "blue", "center", 2300),
            StimulusMetadata(26, "red", "right", 1000),
            StimulusMetadata(27, "green", "left", 1900),
            StimulusMetadata(28, "green", "right", 1550),
            StimulusMetadata(29, "red", "left", 2100),
            StimulusMetadata(30, "blue", "left", 1240),
            StimulusMetadata(31, "green", "center", 1350),
            StimulusMetadata(32, "blue", "right", 1000),
            StimulusMetadata(33, "red", "center", 1750),
            StimulusMetadata(34, "green", "left", 1100),
            StimulusMetadata(35, "red", "right", 1800),
            StimulusMetadata(36, "blue", "center", 1050),
        ]
        self._metadata_cache["simple"] = TestMetadata("simple", simple_stimuli)

        # 2. ТЕСТ С КРАСНЫМ СТИМУЛОМ (color_red/Tst2) - ВСЕ КРАСНЫЕ
        color_red_stimuli = [
            StimulusMetadata(1, "red", "right", 2000, "ЖЖС ЖСЖ ССЖ ЖЖЖ ЖСК"),
            StimulusMetadata(2, "red", "left", 1200, "СЖС ЖСЖ КЖС"),
            StimulusMetadata(3, "red", "right", 2400,
                             "ССЖ ЖСЖ ЖЖС СЖС ЖСЖ СЖК"),
            StimulusMetadata(4, "red", "center", 2800,
                             "ЖЖС СЖС ЖСС СЖЖ ЖСЖ СЖС ЖКЖ"),
            StimulusMetadata(5, "red", "right", 1600, "СЖС ЖСЖ СЖЖ ЖСК"),
            StimulusMetadata(6, "red", "center", 2800,
                             "ЖСЖ ССС СЖЖ СЖС ЖЖЖ ССЖ ЖКС"),
            StimulusMetadata(7, "red", "left", 2000, "СЖС ССС ЖСЖ ССС КЖЖ"),
            StimulusMetadata(8, "red", "left", 1200, "ЖСС ССЖ КЖС"),
            StimulusMetadata(9, "red", "center", 2400,
                             "ЖЖС ССС ЖЖЖ ССЖ ЖЖС СКЖ"),
            StimulusMetadata(10, "red", "right", 1600, "СЖС ЖЖС СЖЖ ЖСК"),
            StimulusMetadata(11, "red", "left", 2800,
                             "ЖЖС ССЖ ЖСЖ ССЖ ЖСЖ ССЖ КЖС"),
            StimulusMetadata(12, "red", "center", 1200, "СЖС ССЖ ЖКС"),
            StimulusMetadata(13, "red", "center", 2000, "ССЖ ЖСС ЖСЖ ЖЖС СКЖ"),
            StimulusMetadata(14, "red", "left", 3200,
                             "СЖС ЖЖС ЖСЖ СЖЖ ССЖ ЖСЖ СЖС КСЖ"),
            StimulusMetadata(15, "red", "right", 2000, "ЖЖС ЖСЖ ССС СЖЖ ЖСК"),
            StimulusMetadata(16, "red", "center", 2800,
                             "СЖС ЖЖС ССС ЖЖЖ ССЖ СЖЖ ЖКС"),
            StimulusMetadata(17, "red", "left", 2000, "ЖЖС ЖСС ССЖ ЖЖС КСЖ"),
            StimulusMetadata(18, "red", "left", 3200,
                             "СЖС ЖЖС ССС ЖСЖ ЖЖЖ СЖС ЖЖС КСЖ"),
            StimulusMetadata(19, "red", "center", 1600, "ЖЖС ССЖ СЖС ЖКС"),
            StimulusMetadata(20, "red", "right", 2400,
                             "СЖС ЖЖС ЖСЖ СЖЖ ССЖ ЖЖК"),
            StimulusMetadata(21, "red", "center", 2000, "ЖЖС ССС ЖЖЖ ССЖ ЖКС"),
            StimulusMetadata(22, "red", "right", 1200, "ССЖ СЖС ЖСК"),
            StimulusMetadata(23, "red", "left", 2400,
                             "ЖЖС ЖСЖ ССЖ ЖСЖ ЖСС КЖЖ"),
            StimulusMetadata(24, "red", "right", 3200,
                             "СЖС ЖЖС ЖСЖ ЖЖС ССЖ ЖСЖ СЖС ЖСК"),
            StimulusMetadata(25, "red", "center", 2000, "ЖЖС ЖСЖ ССЖ ЖСЖ СКС"),
            StimulusMetadata(26, "red", "right", 3200,
                             "СЖС ЖЖС ЖСЖ ССЖ ЖСЖ ССЖ ЖСС СЖК"),
            StimulusMetadata(27, "red", "left", 2000, "ЖЖС ССЖ ЖСЖ СЖС КСЖ"),
            StimulusMetadata(28, "red", "right", 2400,
                             "СЖС ЖСЖ ССЖ ЖСЖ СЖС ЖСК"),
            StimulusMetadata(29, "red", "left", 1600, "ССЖ ЖСЖ СЖС КСЖ"),
            StimulusMetadata(30, "red", "left", 3200,
                             "СЖС ЖЖС ССЖ ЖЖЖ ССЖ ЖЖС ССЖ КЖС"),
            StimulusMetadata(31, "red", "center", 2000, "ЖЖС ССЖ ЖСЖ СЖС ЖКЖ"),
            StimulusMetadata(32, "red", "right", 2400,
                             "СЖС ЖСЖ ССЖ СЖЖ ЖСЖ СЖК"),
            StimulusMetadata(33, "red", "center", 1200, "ЖСС СЖЖ ЖКС"),
            StimulusMetadata(34, "red", "left", 3200,
                             "СЖС ЖЖС ССЖ ЖСС ЖЖЖ ССС ЖЖС КСЖ"),
            StimulusMetadata(35, "red", "right", 2400,
                             "ССС ЖСЖ ССЖ ЖСЖ СЖС ЖСК"),
            StimulusMetadata(36, "red", "center", 1600, "СЖС ЖЖС ССЖ ЖКС"),
        ]
        self._metadata_cache["color_red"] = TestMetadata(
            "color_red", color_red_stimuli)

        # 3. ТЕСТ СО СМЕЩЕНИЕМ (shift/Tst3)
        shift_stimuli = [
            StimulusMetadata(1, "blue", "right", 1600,
                             "КЖС0 ЖСК0 СКЖ0 КЖС3", 3),
            StimulusMetadata(2, "red", "left", 2400,
                             "СЖС0 СКС0 ЖСК0 ССЖ0 КЖС0 ЖКК1", 1),
            StimulusMetadata(3, "red", "right", 1200, "ЖСЖ0 ЖКС0 СЖК3", 3),
            StimulusMetadata(4, "blue", "center", 2400,
                             "ССК0 ЖСЖ0 СЖС0 КСК0 КСЖ0 СКС2", 2),
            StimulusMetadata(5, "green", "right", 1600,
                             "КСЖ0 ЖСС0 СЖК0 КСЖ3", 3),
            StimulusMetadata(6, "green", "center", 2800,
                             "ЖСК0 СЖС0 КСЖ0 ЖСС0 ССЖ0 ЖКК0 КСЖ2", 2),
            StimulusMetadata(7, "red", "left", 1200, "СЖС0 КСЖ0 ЖСК1", 1),
            StimulusMetadata(8, "green", "left", 2000,
                             "СЖС0 ЖКС0 КСЖ0 ССК0 КЖЖ1", 1),
            StimulusMetadata(9, "red", "center", 2400,
                             "КЖС0 ССК0 ЖКС0 ЖЖК0 ССЖ0 КЖК2", 2),
            StimulusMetadata(10, "blue", "right", 2800,
                             "СЖС0 КЖС0 ЖКС0 КСЖ0 КЖС0 ССЖ0 ЖКС3", 3),
            StimulusMetadata(11, "green", "left", 1600,
                             "КЖС0 СКЖ0 ЖЖК0 СКЖ1", 1),
            StimulusMetadata(12, "blue", "center", 1600,
                             "СЖС0 ЖСК0 ССЖ0 ЖКС2", 2),
            StimulusMetadata(13, "red", "center", 3200,
                             "СЖС0 КСК0 ЖКЖ0 КСС0 КЖС0 ССК0 ЖКС0 СЖК2", 2),
            StimulusMetadata(14, "blue", "left", 2400,
                             "СЖК0 КЖС0 ЖСЖ0 ККС0 ЖСЖ0 КЖС1", 1),
            StimulusMetadata(15, "green", "right", 1600,
                             "ЖКК0 КСЖ0 СЖС0 ККЖ3", 3),
            StimulusMetadata(16, "green", "center", 2400,
                             "СЖС0 ЖСК0 СКЖ0 ЖСЖ0 СЖК0 КСЖ2", 2),
            StimulusMetadata(17, "red", "left", 1600,
                             "СЖС0 ЖКК0 КСЖ0 СКК1", 1),
            StimulusMetadata(18, "blue", "left", 2800,
                             "КЖС0 СКЖ0 КЖС0 ЖКЖ0 ССК0 ЖСЖ0 КЖС1", 1),
            StimulusMetadata(19, "red", "center", 1200, "КЖС0 ССЖ0 КЖК2", 2),
            StimulusMetadata(20, "blue", "right", 2000,
                             "СЖС0 ЖСК0 СКЖ0 ЖЖК0 ККС3", 3),
            StimulusMetadata(21, "blue", "center", 2400,
                             "КЖС0 СЖЖ0 ЖСК0 СЖС0 ЖСЖ0 СКС2", 2),
            StimulusMetadata(22, "green", "right", 2800,
                             "СЖС0 СКЖ0 КЖС0 ЖСК0 СКЖ0 ЖСК0 ККЖ3", 3),
            StimulusMetadata(23, "green", "left", 1600,
                             "СКК0 СЖС0 КСЖ0 СКЖ1", 1),
            StimulusMetadata(24, "red", "right", 2800,
                             "КЖС0 ЖКЖ0 ССК0 ЖСЖ0 СКС0 КСЖ0 СЖК3", 3),
            StimulusMetadata(25, "red", "center", 1200, "КЖС0 СКЖ0 КСК2", 2),
            StimulusMetadata(26, "red", "right", 2800,
                             "СКК0 ЖЖС0 ССЖ0 ЖЖК0 КСЖ0 ЖЖС0 ССК3", 3),
            StimulusMetadata(27, "blue", "left", 2000,
                             "КЖС0 ЖСК0 СКЖ0 КСЖ0 ЖКС1", 1),
            StimulusMetadata(28, "green", "right", 2400,
                             "СКС0 КЖС0 ЖКК0 ССЖ0 ЖСК0 СКЖ3", 3),
            StimulusMetadata(29, "blue", "left", 1200, "КЖС0 ЖСЖ0 КЖС1", 1),
            StimulusMetadata(30, "green", "left", 2800,
                             "СЖС0 ЖКК0 СЖС0 ЖКЖ0 ССК0 КЖЖ0 СКЖ1", 1),
            StimulusMetadata(31, "red", "center", 1600,
                             "ККС0 СЖК0 ЖКС0 СЖК2", 2),
            StimulusMetadata(32, "blue", "right", 2800,
                             "СЖК0 КЖС0 ССЖ0 ЖКК0 СЖС0 ЖЖК0 ККС3", 3),
            StimulusMetadata(33, "green", "center", 1600,
                             "ССК0 ЖСЖ0 КСЖ0 СКЖ2", 2),
            StimulusMetadata(34, "blue", "left", 2000,
                             "КЖС0 ЖКЖ0 ССК0 КСЖ0 ЖКС1", 1),
            StimulusMetadata(35, "red", "right", 2800,
                             "СЖК0 ЖКС0 СКЖ0 ЖСК0 КЖС0 ССЖ0 ЖЖК3", 3),
            StimulusMetadata(36, "green", "center", 1200, "ККК0 ЖСК0 СКЖ2", 2),
        ]

        self._metadata_cache["shift"] = TestMetadata("shift", shift_stimuli)

        logger.info("✅ Встроенные метаданные тестирования загружены")

    def load_from_database(self, db_connection):
        """Загрузить метаданные из базы данных"""
        try:
            cursor = db_connection.cursor()

            # Загрузить метаданные тестов
            cursor.execute("""
                           SELECT test_type,
                                  stimulus_number,
                                  color,
                                  position,
                                  prestimulus_interval,
                                  circle_sequence,
                                  shift_parameter
                           FROM test_metadata
                           ORDER BY test_type, stimulus_number
                           """)
            rows = cursor.fetchall()

            if rows:
                # Очистить кэш и перезагрузить из БД
                self._metadata_cache.clear()

                for row in rows:
                    test_type, stimulus_number, color, position, prestimulus_interval, circle_sequence, shift_parameter = row

                    stimulus = StimulusMetadata(
                        stimulus_number=stimulus_number,
                        color=color,
                        position=position,
                        prestimulus_interval=prestimulus_interval,
                        circle_sequence=circle_sequence,
                        shift_parameter=shift_parameter
                    )

                    if test_type not in self._metadata_cache:
                        self._metadata_cache[test_type] = TestMetadata(
                            test_type, [])

                    self._metadata_cache[test_type].stimuli.append(stimulus)

                # Загрузить системные параметры
                cursor.execute(
                    "SELECT parameter_name, parameter_value FROM testing_system_parameters")
                system_params_rows = cursor.fetchall()

                for param_name, param_value in system_params_rows:
                    try:
                        self._system_parameters[param_name] = int(param_value)
                    except ValueError:
                        # Если не число, сохраняем как строку
                        self._system_parameters[param_name] = param_value

                logger.info(f"✅ Метаданные загружены из БД: {len(self._metadata_cache)} тестов, "
                            f"{len(rows)} стимулов, {len(system_params_rows)} параметров")
                return True
            else:
                logger.info(
                    "ℹ️ В БД нет данных метаданных, используются встроенные")
                return False

        except Exception as e:
            logger.error(f"❌ Ошибка загрузки метаданных из БД: {e}")
            # При ошибке используем встроенные данные
            return False

    def get_test_metadata(self, test_type: str) -> Optional[TestMetadata]:
        """Получить метаданные для конкретного теста"""
        return self._metadata_cache.get(test_type)

    def get_stimulus_metadata(self, test_type: str, stimulus_number: int) -> Optional[StimulusMetadata]:
        """Получить метаданные конкретного стимула"""
        test_meta = self.get_test_metadata(test_type)
        if test_meta and 1 <= stimulus_number <= len(test_meta.stimuli):
            return test_meta.get_stimulus(stimulus_number)
        return None

    def get_system_parameter(self, param_name: str, default=None):
        """Получить значение системного параметра"""
        return self._system_parameters.get(param_name, default)

    def get_all_test_types(self) -> List[str]:
        """Получить список всех доступных типов тестов"""
        return list(self._metadata_cache.keys())

    def get_stimulus_count(self, test_type: str) -> int:
        """Получить количество стимулов для типа теста"""
        test_meta = self.get_test_metadata(test_type)
        return len(test_meta.stimuli) if test_meta else 0

    def print_summary(self):
        """Вывести сводку по загруженным метаданным"""
        print("\n📊 СВОДКА МЕТАДАННЫХ ТЕСТИРОВАНИЯ:")
        print("=" * 50)

        for test_type in self.get_all_test_types():
            test_meta = self.get_test_metadata(test_type)
            print(
                f"🎯 {TEST_TYPES.get(test_type, test_type)}: {len(test_meta.stimuli)} стимулов")

            # Статистика по цветам
            color_stats = {}
            for stimulus in test_meta.stimuli:
                color_stats[stimulus.color] = color_stats.get(
                    stimulus.color, 0) + 1

            print(
                f"   🎨 Цвета: {', '.join([f'{STIMULUS_COLORS[color]} ({count})' for color, count in color_stats.items()])}")

            # Показать первые 3 стимула для примера
            print("   📋 Примеры стимулов:")
            for i, stimulus in enumerate(test_meta.stimuli[:3]):
                shift_info = f", смещение={stimulus.shift_parameter}" if stimulus.shift_parameter else ""
                circle_info = f", круги: {stimulus.circle_sequence}" if stimulus.circle_sequence else ""
                print(f"     {i + 1}. {STIMULUS_COLORS[stimulus.color]} {STIMULUS_POSITIONS[stimulus.position]} "
                      f"(ожидание: {stimulus.prestimulus_interval}ms{shift_info}{circle_info})")

            if len(test_meta.stimuli) > 3:
                print(f"     ... и еще {len(test_meta.stimuli) - 3} стимулов")
            print()

        print("⚙️ СИСТЕМНЫЕ ПАРАМЕТРЫ:")
        for param, value in self._system_parameters.items():
            print(f"   • {param}: {value}")
