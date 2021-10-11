export default class Media {
  public static readonly prefix: string = process.env.VUE_APP_MEDIA_PATH;

  public static cover(mangaId: string, version: number): string {
    return `${this.prefix}/${mangaId}/cover.jpg?version=${version}`;
  }

  public static page(
    mangaId: string,
    chapterId: string,
    pageNumber: number,
    version: number,
  ): string {
    return `${this.prefix}/${mangaId}/${chapterId}/${pageNumber}.jpg?version=${version}`;
  }

  public static blob(blobId: string): string {
    return `${this.prefix}/blobs/${blobId}.jpg`;
  }
}
