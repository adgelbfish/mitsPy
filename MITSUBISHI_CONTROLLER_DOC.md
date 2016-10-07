#Documentation for connecting to the Mitsubishi Controllers

##The Basics
Communication with the controllers is done through commands via xml over http to and from the servlet that the Java applet communicates with.

An example command would be a post request to the servlet with the following XML:


```
<?xml version="1.0" encoding="UTF-8"?>
<Packet>
    <Command>
        getRequest
    </Command>
    <DatabaseManager>
        <ControlGroup>
            <MnetGroupList/>
        </ControlGroup>
    </DatabaseManager>
</Packet>
```

the response to that would be something like:

```
<?xml version="1.0" encoding="UTF-8"?>
<Packet>
    <Command>
        getResponse
    </Command>
    <DatabaseManager>
        <ControlGroup>
            <MnetGroupList>
                <MnetGroupRecord
                        Group="???"
                        Model="???"
                        Address="???"/>
                <MnetGroupRecord
                        Group="???"
                        Model="???"
                        Address="???"/>
                <MnetGroupRecord
                        Group="???"
                        Model="???"
                        Address="???"/>
                <MnetGroupRecord
                        Group="???"
                        Model="???"
                        Address="???"/>
            </MnetGroupList>
        </ControlGroup>
    </DatabaseManager>
</Packet>
```

##XML Structure for Mitsubishi Controllers
Note: (triple question marks [`???`] are used in place of items that may be different based on user config)

the first line of the file is the XML prolog. It stays the same and goes like this:
```
<?xml version="1.0" encoding="UTF-8"?>
```
next come the elements (note: you will not find all of the elements in a single request or response):

 - `<Packet>` - the root element
    - `<Command>`
        - `getRequest`
        - `getResponse`
        - `setRequest`
        - `setResponse`
    - `<DatabaseManager>`
        - `<ControlGroup>`
            - `<MnetGroupList>`
                - `<MnetGroupRecord>`
                    - `Group="???"`
                    - `Model="???"`
                    - `Address="???"`
            - `<AreaGroupList>`
                - `<AreaGroupRecord>`
                    - `Area="???"`
                    - `Group="???"`
                    - `ModelID="???"`
            - `<AreaList>`
                - `<AreaRecord>`
                    - `Area="???"`
                    - `AreaName="???"`
            - `<MnetGroupList>`
                - `<MnetGroupRecord>`
                    - `Group="???"`
                    - `Model="???"`
                    - `Address="???"`
            - `<MnetList>`
                - `<MnetRecord>`
                    - `Group="???"`
                    - `GroupNameWeb="???"`
                    - `GroupNameLcd="???"`
            - `<DdcInfoList>`
            - `<ViewInfoList>`
                - `<ViewInfoRecord>`
                    - `Group="???"`
                    - `Icon="???"`
            - `<McList>`
                - `<McNameList>`
        - `<FunctionControl>`
            - `<FunctionList>`
        - `<Mnet>`
            - `Group="???"`
            - `Bulk="???"`
            - `EnergyControl="???"`
            - `RacSW="???"`
        - `<SetbackControl>`
            - `Group="???"`
            - `State="???"`
            - `Hold="???"`
            - `SetTempMax="???"`
            - `SetTempMin="???"`
            - `PreMode="???"`
            - `PreSetTemp="???"`
            - `PreDriveItem="???"`
            - `PreModeItem="???"`
            - `PreSetTempItem="???"`
        - `<ScheduleControl>`
            - `<TodayList>`
                - `Group="???"`
                - `MultiGroup="???"`
                - `<TodayRecord>`
                    - `Index="???"`
                    - `Hour="???"`
                    - `Minute="???"`
                    - `Drive="???"`
                    - `Mode="???"`
                    - `SetTemp="???"`
                    - `SetTempMax="???"`
                    - `SetTempMin="???"`
                    - `SetBackState="???"`
                    - `SetBack="???"`
                    - `DriveItem="???"`
                    - `ModeItem="???"`
                    - `SetTempItem="???"`
            - `<WPatternList>`
                - `Group="???"`
                - `MultiGroup="???"`
                - `Pattern="???"`
            - `<YPatternList>`
                - `Group="???"`
                - `MultiGroup="???"`
                - `Pattern="???"`
                - `<YPatternRecord>`
                    - `Index="???"`
                    - `Hour="???"`
                    - `Minute="???"`
                    - `Drive="???"`
                    - `Mode="???"`
                    - `SetTemp="???"`
                    - `SetTempMax="???"`
                    - `SetTempMin="???"`
                    - `SetBackState="???"`
                    - `SetBack="???"`
                    - `DriveItem="???"`
                    - `ModeItem="???"`
                    - `SetTempItem="???"`
            - `<YearlyList>`
                - `Group="???"`
                - `MultiGroup="???"`
                - `<YearlyRecord>`
                    - `Index="???"`
                    - `Year="???"`
                    - `Month="???"`
                    - `Day="???"`
                    - `Pattern="???"`
        - `<UserAuth>`
            - `User="???"`
            - `Password="???"`
            - `PasswordKey="???"`
            - `Html="???"`
            - `HtmlKey="???"`
            - `AvailableGroup="???"`
            - `UserCategory="???"`
        - `<SystemData>`
            - `Version="???`
            - `TempUnit="???"`
            - `Model="???"`
            - `FilterSign="???"`
            - `ShortName="???"`
            - `DateFormat="???"`
