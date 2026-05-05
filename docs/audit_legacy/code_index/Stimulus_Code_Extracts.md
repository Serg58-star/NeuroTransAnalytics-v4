# Stimulus Code Extracts

## Reactest\Тест 1\simple_test.pas
```pascal
    procedure TimerMaxRedLightTimer(Sender: TObject);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Timer2Timer(Sender: TObject);

...
    ws1 := LeftStr(ws, 1);
    if ws1 = cy then
      CW[n] := 'y'
    else
      if ws1 = cb then

...
    ws1 := LeftStr(ws, 1);
    if ws1 = cy then
      CD[n] := 'y'
    else
      if ws1 = cb then

...
    cnt_prom := 0;
    cnt_kxy  := 0;
    ProgressBar1.Position := cnt_showinfo;
  end;


...

procedure TForm1.FormMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if Button = MouseButton then

...
    PressOnDisc();
    lblInfo.Caption := InfoLabelTextFast;
    ProgressBar1.Position := 100;
    cnt_showinfo := 5000;
    InfoPanel.Visible := True;

```

## Reactest\Тест 2\simple_test.pas
```pascal
    procedure ShowInfoTimerTimer(Sender: TObject);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormKeyPress(Sender: TObject; var Key: Char);


...

  RotatePeriod := strtoint(IniFileCnf.ReadString('T2_CONFIG', 'ROTATE_PERIOD', '500')); // РїРѕР»СѓС‡Р°РµРј РїРµСЂРёРѕРґ РІСЂР°С‰РµРЅРёСЏ РєСЂСѓРіРѕРІ (Рј/СЃ)
  RotationTimer.Interval := RotatePeriod;

  TestType := IniFileCnf.ReadString('T2_TYPE', 'variant', '');

...

procedure TForm1.FormMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if Button = MouseButton then

...
begin
  if TimeShowInfo > 0 then
    ProgressBar1.Position := TimeShowInfo
  else
    if InfoPanel.Visible then begin

```

## Reactest\Тест 3\simple_test.pas
```pascal
    procedure ShowInfoTimerTimer(Sender: TObject);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  private

...
  DCOUNT := StrToInt(IniFileCnf.ReadString('T3_CONFIG', 'NoUchtPOKAZ_COUNT', '1'));

  RotationTimer.Interval := StrToInt(IniFileCnf.ReadString('T3_CONFIG', 'ROTATE_PERIOD', '500')); // РїРѕР»СѓС‡Р°РµРј РїРµСЂРёРѕРґ РІСЂР°С‰РµРЅРёСЏ РєСЂСѓРіРѕРІ (Рј/СЃ)

  for n := 1 to 99 do begin // РїРѕР»СѓС‡РµРЅРёРµ РІ РјР°СЃСЃРёРІ "A" РїРµСЂРµРјРµРЅРЅС‹С…

...

procedure TForm1.FormMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if Button = MouseButton then

...
begin
  if Time_ShowInfo > 0 then
    ProgressBar1.Position := Time_ShowInfo
  else
    if InfoPanel.Visible then begin

```
