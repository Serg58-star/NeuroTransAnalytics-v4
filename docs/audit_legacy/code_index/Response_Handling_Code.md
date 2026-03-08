# Response Handling Code

## Reactest\Тест 1\simple_test.pas
```pascal
    procedure FormDestroy(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure TimerShowInfoTimer(Sender: TObject);
    procedure TimerShowDiscTimer(Sender: TObject);

...
function timeGetMinPeriod(): DWORD;
var
  time: TTimeCaps;
begin
  timeGetDevCaps(Addr(time), SizeOf(time));

...
begin
  timeGetDevCaps(Addr(time), SizeOf(time));
  timeGetMinPeriod := time.wPeriodMin;
end;


...
    DebugPanel.Visible := True;

  MouseButtonStr := Trim(IniFileCnf.ReadString('mouse', 'button', 'mbleft')); // РїРѕР»СѓС‡Р°РµРј РєРЅРѕРїРєСѓ РјС‹С€Рё, РЅР° РєРѕС‚РѕСЂСѓСЋ Р±СѓРґРµС‚ СЂРµР°РіРёСЂРѕРІР°С‚СЊ РїСЂРѕРіСЂР°РјРјР° (РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ - Р»РµРІР°СЏ РєРЅРѕРїРєР°, РґР»СЏ РїСЂР°РІС€Рё)
  if MouseButtonStr = 'mbright' then
    MouseButton := mbright

...
end;

procedure TForm1.FormKeyPress(Sender: TObject; var Key: Char);
begin
  case Key of

```

## Reactest\Тест 2\simple_test.pas
```pascal
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormKeyPress(Sender: TObject; var Key: Char);

  private

...
function timeGetMinPeriod(): DWORD;
var
  time: TTimeCaps;
begin
  timeGetDevCaps(Addr(time), SizeOf(time));

...
begin
  timeGetDevCaps(Addr(time), SizeOf(time));
  timeGetMinPeriod := time.wPeriodMin;
end;


...
  if strtoint(IniFileCnf.ReadString('T2_CONFIG', 'engineering', '0')) = 1 then
    DebugPanel.Visible := True;
  MouseButtonStr := trim(IniFileCnf.ReadString('mouse', 'button', 'mbleft')); // РїРѕР»СѓС‡Р°РµРј РєРЅРѕРїРєСѓ РјС‹С€Рё, РЅР° РєРѕС‚РѕСЂСѓСЋ Р±СѓРґРµС‚ СЂРµР°РіРёСЂРѕРІР°С‚СЊ РїСЂРѕРіСЂР°РјРјР° (РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ - Р»РµРІР°СЏ РєРЅРѕРїРєР°, РґР»СЏ РїСЂР°РІС€Рё)
  if MouseButtonStr = 'mbright' then
    MouseButton := mbright

...
end;

procedure TForm1.FormKeyPress(Sender: TObject; var Key: Char);
begin
  case Key of

```

## Reactest\Тест 3\simple_test.pas
```pascal
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }

...
function timeGetMinPeriod(): DWORD;
var
  time: TTimeCaps;
begin
  timeGetDevCaps(Addr(time), SizeOf(time));

...
begin
  timeGetDevCaps(Addr(time), SizeOf(time));
  timeGetMinPeriod := time.wPeriodMin;
end;


...
    MainPanel.Left := DebugPanel.Left + DebugPanel.Width + 1;
  end;
  MouseButtonStr := Trim(IniFileCnf.ReadString('mouse', 'button', 'mbleft')); // РїРѕР»СѓС‡Р°РµРј РєРЅРѕРїРєСѓ РјС‹С€Рё, РЅР° РєРѕС‚РѕСЂСѓСЋ Р±СѓРґРµС‚ СЂРµР°РіРёСЂРѕРІР°С‚СЊ РїСЂРѕРіСЂР°РјРјР° (РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ - Р»РµРІР°СЏ РєРЅРѕРїРєР°, РґР»СЏ РїСЂР°РІС€Рё)
  if MouseButtonStr = 'mbright' then
    MouseButton := mbright

...
end;

procedure TForm1.FormKeyPress(Sender: TObject; var Key: Char);
begin
  case Key of

```
