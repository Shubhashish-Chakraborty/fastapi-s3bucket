export const getFileType = (url: string) => {
  // presigned s3 links often have query parameters, e.g. ?X-Amz-Algorithm=...
  // we just want the path extension so strip off the querystring first
  let cleanUrl = url

  try {
    // use URL constructor when possible
    const parsed = new URL(url)
    cleanUrl = parsed.pathname // will contain "/path/to/file.ext"
  } catch {
    // if URL constructor fails (e.g. relative paths) fall back to manual split
    cleanUrl = url.split("?")[0]
  }

  const ext = cleanUrl.split(".").pop()?.toLowerCase()

  if (!ext) return "other"

  if (["png", "jpg", "jpeg", "gif", "webp"].includes(ext)) return "image"
  if (["mp4", "webm", "ogg"].includes(ext)) return "video"
  if (["pdf"].includes(ext)) return "pdf"

  return "other"
}
