export function getShowType(item: any): string {
  if (item && item.debugging) {
    if (item.debugging.references && item.debugging.references.length > 0) {
      return "search-reference";
    }
  }
  return "thinking";
}

export function handeLittleTagsData(quote_infos: any[], references: any[], content: string): string {
  if (!content) return "";
  if (!quote_infos || quote_infos.length === 0) return content;

  // 按照位置从大到小排序，避免位置错位
  const sortedQuoteInfos = [...quote_infos].sort((a, b) => b.position - a.position);

  let result = content;
  sortedQuoteInfos.forEach(item => {
    // 提取id数组并转换为字符串
    const tagIds = (item.tag || []).map((tag: any) => tag.id);
    const tagString = `[${tagIds.join(",")}](@ref)`;

    // 在指定位置插入字符串
    result = result.slice(0, item.position) + tagString + result.slice(item.position);
  });

  return result;
}

export const scrollToBottom = (sDom: HTMLElement, sTop: number) => {
  if (!sDom) return;

  sDom.scrollTo({
    top: sTop
    // behavior: 'smooth'
  });
};

export const generateSessionId = () => {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};
