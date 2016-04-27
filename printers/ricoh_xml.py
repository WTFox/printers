__author__ = 'afox'

auth_xml = """\
<?xml version="1.0" encoding="utf-8" ?>
<s:Envelope
    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <s:Body>
        <m:startSession
            xmlns:m="http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory">
            <stringIn>{stringIn}</stringIn>
            <timeLimit>30</timeLimit>
            <lockMode>X</lockMode>
        </m:startSession>
    </s:Body>
</s:Envelope>""".strip()

disconnect_xml = """\
<?xml version="1.0" encoding="utf-8" ?>
 <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
   <m:terminateSession xmlns:m="http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory">
    <sessionId>{sessionId}</sessionId>
   </m:terminateSession>
  </s:Body>
 </s:Envelope>""".strip()

search_xml = """\
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
 <s:Body>
  <m:searchObjects xmlns:m="http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory">
    <sessionId>{stringOut}</sessionId>
   <selectProps xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.w3.org/2001/XMLSchema" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" soap-enc:arrayType="itt:string[1]">
    <item>id</item>
   </selectProps>
    <fromClass>entry</fromClass>
    <parentObjectId></parentObjectId>
    <resultSetId></resultSetId>
   <whereAnd xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/udirectory" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/udirectory" soap-enc:arrayType="itt:queryTerm[1]">
    <item>
     <operator></operator>
     <propName>all</propName>
     <propVal></propVal>
     <propVal2></propVal2>
    </item>
   </whereAnd>
   <whereOr xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/udirectory" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/udirectory" soap-enc:arrayType="itt:queryTerm[1]">
    <item>
     <operator></operator>
     <propName></propName>
     <propVal></propVal>
     <propVal2></propVal2>
    </item>
   </whereOr>
   <orderBy xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/udirectory" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/udirectory" soap-enc:arrayType="itt:queryOrderBy[1]">
    <item>
     <propName></propName>
     <isDescending>false</isDescending>
    </item>
   </orderBy>
    <rowOffset>{rowOffset}</rowOffset>
    <rowCount>{rowCount}</rowCount>
    <lastObjectId>{lastObjectId}</lastObjectId>
   <queryOptions xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" soap-enc:arrayType="itt:property[1]">
    <item>
     <propName></propName>
     <propVal></propVal>
    </item>
   </queryOptions>
  </m:searchObjects>
 </s:Body>
</s:Envelope>""".strip()

get_object_xml = """\
<?xml version="1.0" encoding="utf-8" ?>
<s:Envelope
    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <s:Body>
        <m:getObjectsProps
            xmlns:m="http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory">
            <sessionId>{stringOut}</sessionId>
            <objectIdList
                xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/"
                xmlns:itt="http://www.w3.org/2001/XMLSchema" xsi:type="soap-enc:Array"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:arrayType="itt:string[{objects_length}]">
                {objects}
            </objectIdList>
            <selectProps
                xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/"
                xmlns:itt="http://www.w3.org/2001/XMLSchema"
        xsi:type="soap-enc:Array"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes"
        soap-enc:arrayType="itt:string[12]">
                <item>entryType</item>
                <item>id</item>
                <item>name</item>
                <item>longName</item>
                <item>index</item>
                <item>isDestination</item>
                <item>isSender</item>
                <item>mail:</item>
                <item>mail:address</item>
                <item>mail:parameter</item>
                <item>mail:isDirectSMTP</item>
                <item>tagId</item>
            </selectProps>
            <options
                xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/"
                xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:type="soap-enc:Array"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:arrayType="itt:property[1]">
                <item>
                    <propName></propName>
                    <propVal></propVal>
                </item>
            </options>
        </m:getObjectsProps>
    </s:Body>
</s:Envelope>""".strip()

add_user_xml = """\
<?xml version="1.0" encoding="utf-8" ?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
 <s:Body>
  <m:putObjects xmlns:m="http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory">
   <sessionId>{sessionId}</sessionId>
   <objectClass>entry</objectClass>
   <parentObjectId></parentObjectId>
   <propListList xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:arrayType="">
    <item xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:arrayType="itt:property[9]">
     <item>
      <propName>entryType</propName>
      <propVal>user</propVal>
     </item>
     <item>
      <propName>index</propName>
      <propVal>{index}</propVal>
     </item>
     <item>
      <propName>name</propName>
      <propVal>{name}</propVal>
     </item>
     <item>
      <propName>auth:name</propName>
      <propVal>{auth_name}</propVal>
     </item>
     <item>
      <propName>longName</propName>
      <propVal>{longName}</propVal>
     </item>
     <item>
      <propName>isDestination</propName>
      <propVal>{is_destination}</propVal>
     </item>
     <item>
      <propName>isSender</propName>
      <propVal>{is_sender}</propVal>
     </item>
     <item>
      <propName>mail:</propName>
      <propVal>{mail}</propVal>
     </item>
     <item>
      <propName>mail:address</propName>
      <propVal>{mail_address}</propVal>
     </item>
     <item>
      <propName>tagId</propName>
      <propVal>{tagId}</propVal>
     </item>
    </item>
   </propListList>
  </m:putObjects>
 </s:Body>
</s:Envelope>""".strip()

delete_user_xml = """\
<?xml version="1.0" encoding="utf-8" ?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
 <s:Body>
  <m:deleteObjects xmlns:m="http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory">
   <sessionId>{sessionId}</sessionId>
  <objectIdList xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.w3.org/2001/XMLSchema" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:arrayType="">
   <item>entry:{user_id}</item>
  </objectIdList>
   <options xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:itt="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:type="soap-enc:Array" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:t="http://www.ricoh.co.jp/xmlns/schema/rdh/commontypes" xsi:arrayType="itt:property[1]">
    <item>
     <propName></propName>
     <propVal></propVal>
    </item>
   </options>
  </m:deleteObjects>
 </s:Body>
</s:Envelope>""".strip()

if __name__ == '__main__':
    pass
