# Result Processing Code

## Reactest\Тест 1\simple_test.pas
```pascal
      IniFileRes.WriteString('TEST','POZDNO_POKAZ', inttostr(cnt_err_a));
{$IFNDEF FPC}
      IniFileRes.WriteString('TEST','RESULT', floattostr(round(Xsr)));

      IniFileRes.WriteString('TEST','RESULT1', floattostr(round(Xsr1)));

...
      IniFileRes.WriteString('TEST','KoefVariacii3', floattostr(round(V3)));
{$ELSE}
      IniFileRes.WriteString('TEST','RESULT',  inttostr(round(Xsr)));
      IniFileRes.WriteString('TEST','RESULT1', inttostr(round(Xsr1)));
      IniFileRes.WriteString('TEST','RESULT2', inttostr(round(Xsr2)));

```

## Reactest\Тест 2\simple_test.pas
```pascal
  lblWCOUNT.Caption := inttostr(WCOUNT);

  t1_result := strtofloat(IniFileCnf.ReadString('TEST', 'RESULT', '200')); // РїРѕР»СѓС‡Р°РµРј РєРѕР»РёС‡РµСЃС‚РІРѕ РїРѕСЏРІР»РµРЅРёР№ РєСЂСѓРіР°

  RotatePeriod := strtoint(IniFileCnf.ReadString('T2_CONFIG', 'ROTATE_PERIOD', '500')); // РїРѕР»СѓС‡Р°РµРј РїРµСЂРёРѕРґ РІСЂР°С‰РµРЅРёСЏ РєСЂСѓРіРѕРІ (Рј/СЃ)

...
      // IniFileRes.WriteString('TEST2','POZDNO_POKAZ3',inttostr(sum_err_a3));
      {$IFNDEF FPC}
      IniFileRes.WriteString('TEST2','RESULT', floattostr(round(Xsr)));

      IniFileRes.WriteString('TEST2','RESULT1', floattostr(round(Xsr1)));

...
      IniFileRes.WriteString('TEST2','KoefVariacii3', floattostr(round(V3)));
      {$ELSE}
      IniFileRes.WriteString('TEST2','RESULT', inttostr(round(Xsr)));

      IniFileRes.WriteString('TEST2','RESULT1', inttostr(round(Xsr1)));

```

## Reactest\Тест 3\simple_test.pas
```pascal
  if Trim(IniFileCnf.ReadString('MAINCONFIG', 'BoxingType', '0')) = '0' then
    BoxingStr := 0; // Р•СЃР»Рё BoxingType = 0 С‚Рѕ РєСЂСѓРіРё РЅРµ РґРІРёРіР°СЋС‚СЃСЏ
  t1_result := strtofloat(IniFileCnf.ReadString('TEST', 'RESULT', '200'));
  TestType := Trim(IniFileCnf.ReadString('T3_TYPE', 'variant', ''));
  lblTestType.Caption := TestType;

...

      {$IFNDEF FPC}
      IniFileRes.WriteString('TEST3', 'RESULT', floattostr(round(Xsr)));
      IniFileRes.WriteString('TEST3', 'RESULT1',floattostr(round(Xsr1)));
      IniFileRes.WriteString('TEST3', 'RESULT2',floattostr(round(Xsr2)));

...
      IniFileRes.WriteString('TEST3', 'KoefVariacii3',floattostr(round(V3)));
      {$ELSE}
      IniFileRes.WriteString('TEST3', 'RESULT', inttostr(round(Xsr)));
      IniFileRes.WriteString('TEST3', 'RESULT1',inttostr(round(Xsr1)));
      IniFileRes.WriteString('TEST3', 'RESULT2',inttostr(round(Xsr2)));

```
