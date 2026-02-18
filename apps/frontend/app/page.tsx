"use client"

import { useEffect, useState } from "react"
import axios from "axios"
import { getFileType } from "@/services/getFileType"

type ApiResponse = {
  files: string[]
  count: number
}

export default function Home() {

  const [images, setImages] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchImages = async () => {
    try {
      const res = await axios.get<ApiResponse>("http://localhost:8000/data")
      setImages(res.data.files)
    } catch (err: any) {
      console.error(err)
      setError("Backend is Down!")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchImages()
  }, [])

  return (
    <div className="bg-[#0e0e0e] min-h-screen text-white overflow-hidden">

      {/* Header */}
      <div className="flex mt-5 justify-center items-center">
        <div className="bg-blue-700 hover:p-4 hover:scale-110 transition-all cursor-pointer duration-300 text-xl md:text-3xl font-extrabold p-2 rounded-2xl">
          Files Stored in my S3
        </div>
      </div>

      <div className="p-8">

        {/* Loading */}
        {loading && (
          <div className="text-center text-2xl mt-10 animate-pulse">
            Loading Files...
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="text-center text-red-400 mt-10 text-xl">
            {error}
          </div>
        )}

        {/* Empty */}
        {!loading && images.length === 0 && !error && (
          <div className="text-center text-gray-400 mt-10 text-xl">
            No files found in bucket
          </div>
        )}

        {/* Files Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-10">
          {images.map((url, index) => {
            const type = getFileType(url)

            return (
              <div
                key={index}
                className="bg-[#1a1a1a] rounded-2xl overflow-hidden shadow-lg hover:scale-105 transition duration-300 p-2"
              >

                {/* IMAGE */}
                {type === "image" && (
                  <img
                    src={url}
                    alt={`file-${index}`}
                    className="w-full h-64 object-cover rounded-xl"
                    loading="lazy"
                  />
                )}

                {/* VIDEO */}
                {type === "video" && (
                  <video
                    controls
                    className="w-full h-64 object-cover rounded-xl"
                  >
                    <source src={url} />
                    Your browser does not support video.
                  </video>
                )}

                {/* PDF */}
                {type === "pdf" && (
                  <iframe
                    src={url}
                    className="w-full h-64 rounded-xl bg-white"
                  />
                )}

                {/* OTHER FILES */}
                {type === "other" && (
                  <div className="flex flex-col items-center justify-center h-64">
                    <p className="text-gray-400 mb-3">Unsupported preview</p>
                    <a
                      href={url}
                      target="_blank"
                      className="bg-blue-600 px-4 py-2 rounded-xl hover:bg-blue-500"
                    >
                      Download File
                    </a>
                  </div>
                )}

              </div>
            )
          })}

        </div>

      </div>
    </div>
  )
}
