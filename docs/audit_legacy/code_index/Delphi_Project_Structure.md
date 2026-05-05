# Delphi Project Structure

## Project: test1.dpr (in Reactest\Тест 1)

- **Modules (uses):** {$IFnDEF FPC} {$ELSE}   Interfaces, {$ENDIF}   Forms,   simple_test in 'simple_test.pas' {Form1}


- **Initialization/Forms:**
```pascal
Application.Initialize;
Application.CreateForm(TForm1, Form1);
Application.Run;
```

## Project: test1.dpr (in Reactest\Тест 2)

- **Modules (uses):** {$IFnDEF FPC} {$ELSE}   Interfaces, {$ENDIF}   Forms,   simple_test in 'simple_test.pas' {Form1}


- **Initialization/Forms:**
```pascal
Application.Initialize;
Application.CreateForm(TForm1, Form1);
Application.Run;
```

## Project: test1.dpr (in Reactest\Тест 3)

- **Modules (uses):** {$IFnDEF FPC} {$ELSE}   Interfaces, {$ENDIF}   Forms,   simple_test in 'simple_test.pas' {Form1}


- **Initialization/Forms:**
```pascal
Application.Initialize;
Application.CreateForm(TForm1, Form1);
Application.Run;
```
