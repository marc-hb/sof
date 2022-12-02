

Demo:

```
$ cd sof/tools/NHLT/
$ ./NHLT.py nhlt.dat # sample output below

$ ipython3

from NHLT import *

t = NHLT.NHLT_TABLE.parse_file("nhlt.dat")

print(t) # sample output below

...
```

Interactive use: modify one field and write back:

```
t.EndpointDescriptors[0].FormatsConfigs[1].Format

Out[7]: Container(wFormatTag=65534, nChannels=4, nSamplesPerSec=48000, nAvgBytesPerSec=768000, BlockAlign=16, wBitsPerSample=32, cbSize=22, ValidBitsPerSample=24, dwChannelMask=51, gSubFormat=Container(PCM=b'\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x008\x9bq'))

# Change one value
t.EndpointDescriptors[0].FormatsConfigs[1].Format.nSamplesPerSec=44100

# Write to a new file
new_file = open("new_table.dat", "wb")
new_file.write(NHLT.NHLT_TABLE.build(t))

```


diff -u <(./NHLT.py nhlt.dat ) <(./NHLT.py new_table.dat )

```
--- /dev/fd/63	2022-12-02 08:27:06.778399805 +0000
+++ /dev/fd/62	2022-12-02 08:27:06.778399805 +0000
@@ -248,7 +248,7 @@
                     Format = Container:
                         wFormatTag = 0xFFFE
                         nChannels = 4
-                        nSamplesPerSec = 48000
+                        nSamplesPerSec = 44100
                         nAvgBytesPerSec = 768000
                         BlockAlign = 16
                         wBitsPerSample = 32
```

Sample output
```

Container: 
    NhltTableHeader = Container: 
        acpi_header = Container: 
            Signature = u'NHLT' (total 4)
            Length = 6257
            Revision = 0
            Checksum = 0xDB
            OemId = u'INTEL ' (total 6)
            OemTableID = u'MTL' (total 3)
            OemRevision = 0x00000002
            CreatorID = u'    ' (total 4)
            CreatorRevision = 0x01000013
        ACPI_table_signature_not_NHLT = None
    EndpointCount = 1
    EndpointDescriptors = ListContainer: 
        Container: 
            descLength = 6212
            linkType = (enum) DMIC 2
            InstanceId = 0
            VendorId = 0x8086
            DeviceId = 0xAE20
            RevisionId = 1
            SubsystemId = 1
            DeviceType = 0
            Direction = 1
            VirtualBusId = 0
            EndpointConfig = Container: 
                CapabilitiesSize = 3
                Capabilities = hexundump("""
                0000   00 01 0D                                          ...
                """)
                
            FormatsCount = 2
            FormatsConfigs = ListContainer: 
                Container: 
                    Format = Container: 
                        wFormatTag = 0xFFFE
                        nChannels = 4
                        nSamplesPerSec = 48000
                        nAvgBytesPerSec = 384000
                        BlockAlign = 8
                        wBitsPerSample = 16
                        cbSize = 22
                        ValidBitsPerSample = 16
                        dwChannelMask = 51
                        gSubFormat = Container: 
                            PCM = hexundump("""
                            0000   01 00 00 00 00 00 10 00 80 00 00 AA 00 38 9B 71   .............8.q
                            """)
                            
                    FormatConfiguration = Container: 
                        DmicConfigSize = 3048
                        DmicConfigTODO = hexundump("""
                        0000   01 00 00 00 10 32 FF FF 10 32 FF FF FF FF FF FF   .....2...2......
                        0010   FF FF FF FF 03 00 00 00 03 00 00 00 44 08 11 00   ............D...
                        0020   44 08 11 00 03 00 00 00 01 C0 00 00 00 18 00 0B   D...............
                        0030   00 00 00 00 03 0E 00 00 00 00 00 00 00 00 00 00   ................



                        0B80   FC FF CF B3 E9 03 00 B4 FD 06 40 B4 A2 08 80 B4   ..........@.....
                        0B90   8B 08 C0 B4 C0 06 00 B5 92 03 40 B5 88 FF 8F B5   ..........@.....
                        0BA0   3F FB CF B5 51 F7 0F B6 3B F4 4F B6 4A F2 8F B6   ?...Q...;.O.J...
                        0BB0   97 F1 CF B6 0B F2 0F B7 6C F3 4F B7 67 F5 8F B7   ........l.O.g...
                        0BC0   A8 F7 CF B7 E2 F9 0F B8 DD FB 4F B8 76 FD 8F B8   ..........O.v...
                        0BD0   A2 FE CF B8 67 FF 0F B9 D7 FF 4F B9 0A 00 80 B9   ....g.....O.....
                        0BE0   18 00 C0 B9 1B 00 00 BA                           ........
                        """)
                        
                Container: 
                    Format = Container: 
                        wFormatTag = 0xFFFE
                        nChannels = 4
                        nSamplesPerSec = 48000
                        nAvgBytesPerSec = 768000
                        BlockAlign = 16
                        wBitsPerSample = 32
                        cbSize = 22
                        ValidBitsPerSample = 24
                        dwChannelMask = 51
                        gSubFormat = Container: 
                            PCM = hexundump("""
                            0000   01 00 00 00 00 00 10 00 80 00 00 AA 00 38 9B 71   .............8.q
                            """)
                            
                    FormatConfiguration = Container: 
                        DmicConfigSize = 3048
                        DmicConfigTODO = hexundump("""
                        0000   01 00 00 00 10 32 FF FF 10 32 FF FF FF FF FF FF   .....2...2......
                        0010   FF FF FF FF 03 00 00 00 03 00 00 00 44 08 19 00   ............D...
                        0020   44 08 11 00 03 00 00 00 01 C0 00 00 00 18 00 0B   D...............
                        0030   00 00 00 00 03 0E 00 00 00 00 00 00 00 00 00 00   ................
                        0040   00 00 00 00 00 00 00 00 31 00 00 00 76 00 01 00   ........1...v...
```
