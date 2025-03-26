from typing import Any, Dict, List, Optional
import requests
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("pubchem")

# Constants
USER_AGENT = "pubchem-api-client/1.0"

# API请求函数
async def get_cid_by_keyword(keyword: str) -> Optional[List[int]]:
    """
    使用PubChem API，通过关键词查询CID
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    endpoint = f"/compound/name/{keyword}/cids/JSON"
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("IdentifierList", {}).get("CID", None)
    except requests.exceptions.RequestException:
        return None

async def get_sid_by_keyword(keyword: str) -> Optional[List[int]]:
    """
    使用PubChem API，通过关键词查询SID
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    endpoint = f"/substance/name/{keyword}/sids/JSON"
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("IdentifierList", {}).get("SID", None)
    except requests.exceptions.RequestException:
        return None

async def get_compound_data_by_cid(cid: int) -> Optional[Dict[str, Any]]:
    """
    使用PubChem API，通过CID查询化学物质的详细信息
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound"
    endpoint = f"/{cid}/JSON"
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

async def get_substance_data_by_sid(sid: int) -> Optional[Dict[str, Any]]:
    """
    使用PubChem API，通过SID查询物质的详细信息
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance"
    endpoint = f"/{sid}/JSON"
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# 提取类函数
def extract_first_cas(data: Dict[str, Any]) -> Optional[str]:
    """从PubChem API返回的数据中提取第一个CAS Number"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Names and Identifiers":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "Other Identifiers":
                        subsubsection = subsection.get('Section', [])
                        for info in subsubsection:
                            if info.get('TOCHeading') == "CAS":
                                string_with_markup = info.get('Information', {})[0].get('Value', []).get('StringWithMarkup', [])
                                if string_with_markup:
                                    return string_with_markup[0].get('String')
        return None
    except Exception:
        return None

def extract_Weight(data: Dict[str, Any]) -> Optional[str]:
    """提取Molecular Weight"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Chemical and Physical Properties":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "Computed Properties":
                        subsubsection = subsection.get('Section', [])
                        for info in subsubsection:
                            if info.get('TOCHeading') == "Molecular Weight":
                                string_with_markup = info.get('Information', {})[0].get('Value', []).get('StringWithMarkup', [])
                                if string_with_markup:
                                    return string_with_markup[0].get('String')
        return None
    except Exception:
        return None

def extract_Molecular_Formula(data: Dict[str, Any]) -> Optional[str]:
    """提取Molecular Formula"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Names and Identifiers":
                subsections = section.get('Section', [])
                for subsection in subsections:
                    if subsection.get('TOCHeading') == "Molecular Formula":
                        information = subsection.get('Information', [])
                        if information:
                            string_with_markup = information[0].get('Value', {}).get('StringWithMarkup', [])
                            if string_with_markup:
                                return string_with_markup[0].get('String')
        return None
    except Exception:
        return None

def extract_Smiles(data: Dict[str, Any]) -> Optional[str]:
    """提取SMILES"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Names and Identifiers":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "Computed Descriptors":
                        subsubsection = subsection.get('Section', [])
                        for info in subsubsection:
                            if info.get('TOCHeading') == "SMILES":
                                string_with_markup = info.get('Information', {})[0].get('Value', []).get('StringWithMarkup', [])
                                if string_with_markup:
                                    return string_with_markup[0].get('String')
        return None
    except Exception:
        return None

def extract_synonyms(data: Dict[str, Any]) -> Optional[List[str]]:
    """提取Synonyms"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Names and Identifiers":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "Synonyms":
                        subsection = subsection.get('Section', [])
                        if isinstance(subsection, list):
                            subsection_1 = subsection[0]
                        else:
                            subsection_1 = subsection
                        synonyms = []
                        infos = subsection_1.get('Information', [])
                        for info in infos: 
                            string_with_markup = info.get('Value', {}).get('StringWithMarkup', [])
                            for string in string_with_markup:
                                synonyms.append(string.get('String'))
                        return synonyms[:10]  # 取前10个Synonyms
        return None
    except Exception:
        return None

def extract_InchI_Key(data: Dict[str, Any]) -> Optional[str]:
    """提取InchI Key"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Names and Identifiers":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "Computed Descriptors":
                        subsubsection = subsection.get('Section', [])
                        for info in subsubsection:
                            if info.get('TOCHeading') == "InChIKey":
                                string_with_markup = info.get('Information', {})[0].get('Value', []).get('StringWithMarkup', [])
                                if string_with_markup:
                                    return string_with_markup[0].get('String')
        return None
    except Exception:
        return None

def extract_IUPAC_Name(data: Dict[str, Any]) -> Optional[str]:
    """提取IUPAC Name"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Names and Identifiers":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "Computed Descriptors":
                        subsubsection = subsection.get('Section', [])
                        for info in subsubsection:
                            if info.get('TOCHeading') == "IUPAC Name":
                                string_with_markup = info.get('Information', {})[0].get('Value', []).get('StringWithMarkup', [])
                                if string_with_markup:
                                    return string_with_markup[0].get('String')
        return None
    except Exception:
        return None

def extract_ATC_Code(data: Dict[str, Any]) -> Optional[str]:
    """提取ATC Code"""
    try:
        sections = data.get('Record', {}).get('Section', [])
        for section in sections:
            if section.get('TOCHeading') == "Pharmacology and Biochemistry":
                for subsection in section.get('Section', []):
                    if subsection.get('TOCHeading') == "ATC Code":
                        atc_codes = []
                        for info in subsection.get('Information', []):
                            atc_codes.append(info.get('Value', {}).get('StringWithMarkup', [])[0].get('String'))
                        return atc_codes[0]
        return None
    except Exception:
        return None

def extract_name(data: Dict[str, Any]) -> Optional[str]:
    """提取chemical name"""
    try:
        return data.get('Record', {}).get('RecordTitle', None)
    except Exception:
        return None

@mcp.tool()
async def get_chemical_info(name: str) -> str:
    """
    获取化学物质的详细信息
    
    Args:
        name: 化学物质名称
    """
    result = {
        'drug_name': "",
        'CAS Number': "",
        'Molecular Weight': "",
        'Molecular Formula': "",
        'Smiles': "",
        'Synonyms': "",
        'InchI Key': "",
        'IUPAC Name': "",
        'ATC Code': "",
        'status': 'success',
        'message': "",
        'reference_links': ""
    }
    
    # 首先尝试通过关键词获取CID
    cids = await get_cid_by_keyword(str(name))
    
    if cids:
        cid = cids[0]
        result['ID'] = cid
        result['ID_Type'] = 'CID'
        compound_data = await get_compound_data_by_cid(cid)
        result['reference_links'] = f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"
        
        if compound_data:
            result['drug_name'] = extract_name(compound_data)
            result['CAS Number'] = extract_first_cas(compound_data)
            result['Molecular Weight'] = extract_Weight(compound_data)
            result['Molecular Formula'] = extract_Molecular_Formula(compound_data)
            result['Smiles'] = extract_Smiles(compound_data)
            result['Synonyms'] = extract_synonyms(compound_data)
            result['InchI Key'] = extract_InchI_Key(compound_data)
            result['IUPAC Name'] = extract_IUPAC_Name(compound_data)
            result['ATC Code'] = extract_ATC_Code(compound_data)
    else:
        # 如果没有CID，尝试获取SID
        sids = await get_sid_by_keyword(str(name))
        if sids:
            sid = sids[0]
            result['ID'] = sid
            result['ID_Type'] = 'SID'
            result['reference_links'] = f"https://pubchem.ncbi.nlm.nih.gov/substance/{sid}"
            substance_data = await get_substance_data_by_sid(sid)
            
            if substance_data:
                result['CAS Number'] = extract_first_cas(substance_data)
        else:
            result['status'] = 'error'
            result['message'] = 'No CID or SID found in PubChem'
    
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
async def search_chemical_by_cas(cas_number: str) -> str:
    """
    通过CAS号搜索化学物质信息
    
    Args:
        cas_number: 化学物质的CAS号
    """
    # 使用CAS号作为关键词搜索
    return await get_chemical_info(cas_number)

def main():
    """命令行入口点"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
